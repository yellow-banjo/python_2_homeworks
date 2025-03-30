import os
import multiprocessing
import time
import threading
import codecs
from datetime import datetime

LOG_FILE = "artifacts/hw_4_3_results.log"

def log_action(process_name, action, message):
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    with open(LOG_FILE, "a") as log:
        log.write(f"[{timestamp}] - [{process_name}] - {action}: {message}\n")

def process_a(input_queue, output_queue):
    while True:
        if not input_queue.empty():
            message = input_queue.get()
            log_action("A", "Received", message)
            
            if message == "exit":
                output_queue.put("exit")  
                log_action("A", "Sent exit signal", "to B")
                break
                
            processed = message.lower()
            time.sleep(5)
            output_queue.put(processed)
            log_action("A", "Processed and sent", processed)

def process_b(input_queue, output_queue):
    while True:
        message = input_queue.get()
        log_action("B", "Received", message)
        
        if message == "exit":
            output_queue.put(("exit", ""))  
            log_action("B", "Sent exit signal", "to Main")
            break
            
        encoded = codecs.encode(message, 'rot13')
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        output_queue.put((timestamp, encoded))
        log_action("B", "Encoded and sent", encoded)

def main_process():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    main_to_a = multiprocessing.Queue()
    a_to_b = multiprocessing.Queue()
    b_to_main = multiprocessing.Queue()

    pa = multiprocessing.Process(target=process_a, args=(main_to_a, a_to_b))
    pb = multiprocessing.Process(target=process_b, args=(a_to_b, b_to_main))
    pa.start()
    pb.start()

    stop_event = threading.Event()

    def response_listener():
        with open(LOG_FILE, "a") as log:
            while not stop_event.is_set():
                if not b_to_main.empty():
                    data = b_to_main.get()
                    if data[0] == "exit":
                        break
                    timestamp, message = data
                    log.write(f"[{timestamp}] - [MAIN] - Main received: {message}\n")

    listener = threading.Thread(target=response_listener)
    listener.start()

    try:
        while True:
            msg = input("Enter the message or exit: ")
            ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            
            with open(LOG_FILE, "a") as log:
                log.write(f"[{ts}] - [MAIN] - Main sent: {msg}\n")
            
            main_to_a.put(msg)
            
            if msg == "exit":
                time.sleep(1)
                break

    except KeyboardInterrupt:
        main_to_a.put("exit")
    finally:
        stop_event.set()
        listener.join()
        pa.join()
        pb.join()

if __name__ == "__main__":
    main_process()