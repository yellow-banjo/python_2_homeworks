import time
import multiprocessing
import math
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from collections import defaultdict
from tabulate import tabulate


def compute_chunk(f, a, step, start_i, end_i):
    chunk_acc = 0.0
    for i in range(start_i, end_i):
        chunk_acc += f(a + i * step) * step
    return chunk_acc

def integrate(manager, f, a, b, *, n_jobs=1, n_iter=10000000):
    start_time = time.time()
    step = (b - a) / n_iter
    chunk_size = n_iter // n_jobs

    with manager(max_workers=n_jobs) as executor:
        futures = []
        for j in range(n_jobs):
            start = j * chunk_size
            end = start + chunk_size
            if j == n_jobs - 1:
                end = n_iter
            futures.append(executor.submit(compute_chunk, f, a, step, start, end))

        total = 0.0
        for future in as_completed(futures):
            total += future.result()
    end_time = time.time()
    return end_time - start_time

def main():
    results = defaultdict(list)
    managers = [ProcessPoolExecutor, ThreadPoolExecutor]
    for manager in managers:
        for i in range(1, 2 * multiprocessing.cpu_count() + 1):
            res = integrate(manager, math.cos, 0, math.pi / 2, n_jobs=i, n_iter=10**8)
            results[manager.__name__].append(res)

    table_data = []
    for key, value in results.items():
        line = [key]
        line.extend(value)
        table_data.append(line)


    headers = ['manager']
    headers.extend(range(1, 2 * multiprocessing.cpu_count() + 1))

    with open("artifacts/hw_4_2_results.txt", "w") as f:
        f.write(tabulate(table_data, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    main()