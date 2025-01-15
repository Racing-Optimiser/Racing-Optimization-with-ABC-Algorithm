from ABC_algorithm2 import abc_algorithm_demo
import psutil
import os
import time
import csv

def monitor_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss / (1024)  # Zwraca pamięć w MB


def save_results_to_csv(data, filename="Results/5iter5bees5foodx2.csv"):
   
    
    transposed_data = list(zip(*data))
    
  
    headers = [f"Test {i+1}" for i in range(len(transposed_data[0]))]
    
   
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  
        writer.writerows(transposed_data)  

    
# Uruchomienie algorytmu
if __name__ == "__main__":
    tested_solutions = []
    avg_memory = 0
    avg_time = 0
    start_time_testing = time.perf_counter()
    for i in range(2):
        start_memory = monitor_memory()
        start_time = time.perf_counter()
        best_solutions, best_strategies = abc_algorithm_demo(5, 5, 5, 1) # Maksymalna liczba iteracji # Liczba pszczół  # Limit wyczerpania źródła pożywienia
        stop_time = time.perf_counter()
        end_memory = monitor_memory()

        tested_solutions.append(best_solutions)
        avg_memory += end_memory - start_memory
        avg_time += stop_time - start_time
    stop_time_testing = time.perf_counter()
    save_results_to_csv(tested_solutions)