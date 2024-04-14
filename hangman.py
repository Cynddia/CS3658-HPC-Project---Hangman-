import random
import sys
import time
from multiprocessing import Pool
import matplotlib.pyplot as plt


def simulate_hangman_game(word_to_guess, guessed_letters):

    attempts_left = 6
    current_word = ['_'] * len(word_to_guess)


    while attempts_left > 0 and '_' in current_word:


        if '_' not in current_word:
            break

        if guessed_letters:
            guess = guessed_letters.pop()
        else:
            break  


        guessed_letters.add(guess)

        if guess in word_to_guess:
            for i, letter in enumerate(word_to_guess):
                if letter == guess:
                    current_word[i] = guess
        else:
            attempts_left -= 1


    if '_' not in current_word:
        return 1  # Successful game
    else:
        return 0  # Unsuccessful game


def simulate_hangman_games_parallel(word_list, num_games):
    with Pool() as pool:
        results = pool.starmap(simulate_hangman_game, [(random.choice(word_list), set()) for _ in range(num_games)])  # Pass an empty set as guessed letters
    return results

if __name__ == "__main__":
    word_list = ["apple", "banana", "cherry", "date", "elderberry"]
    num_games_list = [1, 2, 3, 4, 5]
    processing_elements_list = [1, 2, 3, 4, 5]

    speed_up_results = []
    parallel_efficiency_results = []

    for num_games in num_games_list:
        for p in processing_elements_list:
            start_time = time.time()
            simulate_hangman_games_parallel(word_list, num_games)
            end_time = time.time()
            execution_time_single_process = end_time - start_time

            start_time = time.time()
            simulate_hangman_games_parallel(word_list, num_games * p)
            end_time = time.time()
            execution_time_parallel = end_time - start_time

            speed_up = execution_time_single_process / execution_time_parallel
            parallel_efficiency = (speed_up / p) * 100

            speed_up_results.append(speed_up)
            parallel_efficiency_results.append(parallel_efficiency)

    # Generate Graph 1: N vs Speed Up
    plt.figure(figsize=(10, 6))
    plt.plot(num_games_list, speed_up_results[:len(num_games_list)], marker='o')
    plt.xlabel('Number of Games (N)')
    plt.ylabel('Speed Up')
    plt.title('Number of Games vs Speed Up')
    plt.grid(True)
    plt.show()

    # Generate Graph 2: N vs Parallel Efficiency
    plt.figure(figsize=(10, 6))
    plt.plot(num_games_list, parallel_efficiency_results[:len(num_games_list)], marker='o')
    plt.xlabel('Number of Games (N)')
    plt.ylabel('Parallel Efficiency (%)')
    plt.title('Number of Games vs Parallel Efficiency')
    plt.grid(True)
    plt.show()

    print("Advantages of using HPC architectures:")
    print("- High Performance: HPC architectures utilize parallel processing, resulting in faster execution of tasks.")
    print("- Scalability: HPC systems can scale up to accommodate larger problem sizes or scale out to handle multiple tasks concurrently.")
    print("- Resource Utilization: HPC systems efficiently utilize resources by distributing workloads across multiple processing elements.")
