import random
import sys
import time
from multiprocessing import Pool
import matplotlib.pyplot as plt

def simulate_hangman_game(word_to_guess):
    attempts_left = 6
    guessed_letters = set()
    current_word = ['_'] * len(word_to_guess)


    while attempts_left > 0 and '_' in current_word:
        guess = random.choice([letter for letter in 'abcdefghijklmnopqrstuvwxyz' if letter not in guessed_letters])
        guessed_letters.add(guess)

        if guess in word_to_guess:
            for i, letter in enumerate(word_to_guess):
                if letter == guess:
                    current_word[i] = guess
        else:
            attempts_left -= 1

    if '_' not in current_word:
        return 1  # Win
    else:
        return 0  # Loss

def simulate_hangman_games(word_list_chunk):
    wins = 0
    total_games = len(word_list_chunk)
    for word in word_list_chunk:
        wins += simulate_hangman_game(word)
    return wins, total_games

if __name__ == "__main__":
    word_list = ["apple", "banana", "cherry", "date", "elderberry"] * 10000  # Extend for more games
    num_games = len(word_list)

    num_chunks = 4  # Number of processes
    chunk_size = len(word_list) // num_chunks
    word_list_chunks = [word_list[i:i+chunk_size] for i in range(0, len(word_list), chunk_size)]

    start_time = time.time()
    with Pool(num_chunks) as pool:
        results = pool.map(simulate_hangman_games, word_list_chunks)
    end_time = time.time()

    total_wins = sum(result[0] for result in results)
    total_games = sum(result[1] for result in results)

    print(f"Total wins: {total_wins}")
    print(f"Total games played: {total_games}")
    print(f"Win rate: {total_wins / total_games * 100:.2f}%")
    print(f"Total time for {total_games} games: {end_time - start_time} seconds")

    
    num_games_list = [num_games]
    processing_elements_list = [1, 2, 3, 4]

    speed_up_results = []
    parallel_efficiency_results = []

    for p in processing_elements_list:
        start_time = time.time()
        with Pool(p) as pool:
            results = pool.map(simulate_hangman_games, word_list_chunks)
        end_time = time.time()

        total_time_parallel = end_time - start_time

        speed_up = (end_time - start_time) / (total_games * num_chunks)
        parallel_efficiency = speed_up / p * 100

        speed_up_results.append(speed_up)
        parallel_efficiency_results.append(parallel_efficiency)

    # Generate Graph 1: N vs Speed Up
    plt.figure(figsize=(10, 6))
    plt.plot(processing_elements_list, speed_up_results, marker='o')
    plt.xlabel('Number of Processing Elements (p)')
    plt.ylabel('Speed Up')
    plt.title('Number of Processing Elements vs Speed Up')
    plt.grid(True)
    plt.show()

    # Generate Graph 2: N vs Parallel Efficiency
    plt.figure(figsize=(10, 6))
    plt.plot(processing_elements_list, parallel_efficiency_results, marker='o')
    plt.xlabel('Number of Processing Elements (p)')
    plt.ylabel('Parallel Efficiency (%)')
    plt.title('Number of Processing Elements vs Parallel Efficiency')
    plt.grid(True)
    plt.show()
