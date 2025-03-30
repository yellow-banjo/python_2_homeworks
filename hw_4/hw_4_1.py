import time
import threading
import multiprocessing


def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n-1) + fib(n-2)

def run_sync(n, times=10):
    print('sync started')
    start = time.time()
    for _ in range(times):
        fib(n)
    end = time.time()
    print("sync finish! Total_time =", end - start)  
    return end - start

def run_threads(n, times=10):
    print('threads started')
    threads = []
    start = time.time()
    
    for _ in range(times):
        t = threading.Thread(target=fib, args=(n,))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    end = time.time()
    print("threads finish! Total_time =", end - start)  
    return end - start


def run_processes(n, times=10):
    print('processes started')
    processes = []
    start = time.time()
    
    for _ in range(times):
        p = multiprocessing.Process(target=fib, args=(n,))
        p.start()
        processes.append(p)
    
    for p in processes:
        p.join()
    end = time.time()
    print("processes finish! Total_time =", end - start)  
    return end - start


if __name__ == '__main__':
    n = 35
    times = 10
    results = {"sync_time": run_sync(n, times),
               "threads_time": run_threads(n, times),
               "processes_time": run_processes(n, times)
               }
    
    msg = f"n = {n}, times = {times} \n"
    msg += "="*25 + "\n"
    for key, value in results.items():
        msg += f"{key:<14} | {value:<5.4} s\n"
    msg += "="*25 + "\n"
    print(msg)

    with open('artifacts/hw_4_1_results.txt', 'w') as f:
        f.write(msg)
