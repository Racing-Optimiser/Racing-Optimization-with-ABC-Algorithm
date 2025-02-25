from ABC_algorithm2 import abc_algorithm_demo
import psutil
import os
import time
import csv
import thread
from thread import Thread
# from queue import Queue
from multiprocessing import Process, Queue, Pool

def monitor_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss / (1024)  # Zwraca pamięć w MB


def save_results_to_csv(data, filename="Results/multithread30iter30bees30foodx50.csv"):
   
    
    transposed_data = list(zip(*data))
    
  
    headers = [f"Test {i+1}" for i in range(len(transposed_data[0]))]
    
   
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  
        writer.writerows(transposed_data)  

def multi_thread_tests(tests,iter,bees,food,race_idx):
    
    # threads = []
    # queue_tests = Queue()
    # tested_solutions = []
    # start_time = time.perf_counter()
    # for _ in range(tests):
    #     thread = Process(target=abc_algorithm_demo,args=(iter,bees,food,race_idx,queue_tests))
    #     threads.append(thread)
    #     thread.start()
    
    # for thread in threads:
    #     thread.join()

    # # while not queue_tests.empty():
    # #     tested_solutions.append(queue_tests.get())
    
    # queue_tests.close()
    # queue_tests.join_thread()

    with Pool() as pool:
        results = pool.starmap(abc_algorithm_demo, [(iter, bees, food, race_idx) for _ in range(tests)])

    
    return results
    
# Uruchomienie algorytmu
if __name__ == "__main__":
    tested_solutions = []
    avg_memory = 0
    avg_time = 0
    start_time_testing = time.perf_counter()
    start_time = time.perf_counter()
    results = multi_thread_tests(50,30,30,30,1)
    stop_time = time.perf_counter()

    for i in range(len(results)):
        tested_solutions.append(results[i][0])

    # for i in range(50):
    #     start_memory = monitor_memory()
    #     start_time = time.perf_counter()
    #     best_solutions, best_strategies, clct, clcm = abc_algorithm_demo(30, 30, 30, 1) # Maksymalna liczba iteracji # Liczba pszczół  # Limit wyczerpania źródła pożywienia
    #     stop_time = time.perf_counter()
    #     end_memory = monitor_memory()

    #     tested_solutions.append(best_solutions)
    #     avg_memory += end_memory - start_memory
    #     avg_time += stop_time - start_time
    # stop_time_testing = time.perf_counter()
    
    save_results_to_csv(tested_solutions)

    # print(f"Memory used: {avg_memory/50:.2f} KB")
    # print(f"Execution time: {avg_time/50}")
    # print(f"Execution time all: {stop_time_testing - start_time_testing}")

    czas = stop_time - start_time

    print(f"Execution time all: {czas}")