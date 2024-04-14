import multiprocessing
from collections import defaultdict
import time
import random
import string
import matplotlib.pyplot as plt

def is_valid_word(word):
    return all(char in string.ascii_lowercase for char in word)

def update_word_letter_counts(chunk):
    letter_counts = defaultdict(int)
    for word in chunk:
        if is_valid_word(word):
            for letter in word:
                letter_counts[letter] += 1
    return letter_counts

def parallel_letter_selection(word_list, guessed_letters, num_games, num_processes):
    start_time = time.time()
    games_won = 0
    
    chunk_size = max(len(guessed_letters) // num_processes, 1)
    
    # Parallelize dividing the word list into chunks
    chunks = [word_list[i:i+chunk_size] for i in range(0, len(word_list), chunk_size)]
    

    with multiprocessing.Pool(processes=num_processes) as pool:
        for _ in range(num_games):
            results = pool.map(update_word_letter_counts, chunks)
            
            
            total_counts = defaultdict(int)
            for counts in results:
                for letter, count in counts.items():
                    total_counts[letter] += count
            
            
            most_common_letter = max(total_counts, key=total_counts.get)
            
            
            if most_common_letter in guessed_letters:
                games_won += 1
            else:
                guessed_letters.append(most_common_letter)
                
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    return elapsed_time, games_won

def calculate_speedup(N, sequential_time, parallel_time):
    return sequential_time / parallel_time

def calculate_parallel_efficiency(speedup, num_processes):
    return (speedup / num_processes) * 100

if __name__ == '__main__':
    word_list = ["apple", "banana", "orange", "grape", "kiwi"]
    guessed_letters = ['a', 'e']
    num_games = 100
    num_processes = multiprocessing.cpu_count()
    
    N_values = [10, 100, 1000, 10000]  
    
   
    speedup_values = []
    parallel_efficiency_values = []
    
    for N in N_values:
        word_list = ["".join(random.choices(string.ascii_lowercase, k=random.randint(1, 10))) for _ in range(N)]
        
        # Sequential execution
        start_time_seq = time.time()
        for _ in range(num_games):
            update_word_letter_counts(word_list)
        end_time_seq = time.time()
        sequential_time = end_time_seq - start_time_seq
        
        # Parallel execution
        elapsed_time, _ = parallel_letter_selection(word_list, guessed_letters, num_games, num_processes)
        
        # speedup and parallel efficiency
        speedup = calculate_speedup(N, sequential_time, elapsed_time)
        parallel_efficiency = calculate_parallel_efficiency(speedup, num_processes)
        
        speedup_values.append(speedup)
        parallel_efficiency_values.append(parallel_efficiency)
        
    # Graph 1: N vs Speed Up
    plt.plot(N_values, speedup_values, marker='o')
    plt.xlabel('Problem Size (N)')
    plt.ylabel('Speed Up')
    plt.title('N vs Speed Up')
    plt.grid(True)
    plt.show()
    
    # Graph 2: For different numbers of processing elements, Plot parallel efficiency with respect to N
    plt.plot(N_values, parallel_efficiency_values, marker='o', label='Parallel Efficiency')
    plt.xlabel('Problem Size (N)')
    plt.ylabel('Parallel Efficiency (%)')
    plt.title('N vs Parallel Efficiency')
    plt.grid(True)
    plt.legend()
    plt.show()
