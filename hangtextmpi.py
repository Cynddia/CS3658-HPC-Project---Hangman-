from mpi4py import MPI
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

def parallel_letter_selection(word_list, guessed_letters, num_games):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    start_time = time.time()
    games_won = 0
    
    chunk_size = max(len(guessed_letters) // size, 1)
    chunks = [word_list[i:i+chunk_size] for i in range(rank * chunk_size, (rank + 1) * chunk_size)]
    
    results = []
    for _ in range(num_games):
        local_counts = update_word_letter_counts(chunks)
        all_counts = comm.gather(local_counts, root=0)
        
        if rank == 0:
            total_counts = defaultdict(int)
            for counts in all_counts:
                for letter, count in counts.items():
                    total_counts[letter] += count
            
            if total_counts:  # Check if the dictionary is not empty
                most_common_letter = max(total_counts, key=total_counts.get)
                if most_common_letter in guessed_letters:
                    games_won += 1
                else:
                    guessed_letters.append(most_common_letter)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    if rank == 0:
        return elapsed_time, games_won
    else:
        return None, None

if __name__ == '__main__':
    word_list = ["apple", "banana", "orange", "grape", "kiwi"]
    guessed_letters = ['a', 'e']
    num_games = 100
    
    N_values = [10, 100, 1000, 10000]  
    
    speedup_values = []
    parallel_efficiency_values = []
    
    markers = ['o', 's', '^', 'd']
    
    for i, N in enumerate(N_values):
        word_list = ["".join(random.choices(string.ascii_lowercase, k=random.randint(1, 10))) for _ in range(N)]
        
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        size = comm.Get_size()

        # Sequential execution
        if rank == 0:
            start_time_seq = time.time()
            for _ in range(num_games):
                update_word_letter_counts(word_list)
            end_time_seq = time.time()
            sequential_time = end_time_seq - start_time_seq
        
        # Parallel execution
        elapsed_time, games_won = parallel_letter_selection(word_list, guessed_letters, num_games)
        elapsed_time = comm.bcast(elapsed_time, root=0)
        games_won = comm.reduce(games_won, op=MPI.SUM, root=0)
        
        # speedup and parallel efficiency
        if rank == 0:
            if elapsed_time == 0:
                speedup = 0
            else:
                speedup = sequential_time / elapsed_time
            parallel_efficiency = (speedup / size) * 100
            
            speedup_values.append(speedup)
            parallel_efficiency_values.append(parallel_efficiency)
        
    # Graph 1: N vs Speed Up
    plt.plot(N_values, speedup_values, marker='o', linestyle='-', label='Speed Up')
    plt.xlabel('Problem Size (N)')
    plt.ylabel('Speed Up')
    plt.title('N vs Speed Up')
    plt.grid(True)
    plt.legend()
    plt.show()
    
    # Graph 2: For different numbers of processing elements, Plot parallel efficiency with respect to N
    plt.plot(N_values, parallel_efficiency_values, marker='o', linestyle='-', label='Parallel Efficiency')
    plt.xlabel('Problem Size (N)')
    plt.ylabel('Parallel Efficiency (%)')
    plt.title('N vs Parallel Efficiency')
    plt.grid(True)
    plt.legend()
    plt.show()
