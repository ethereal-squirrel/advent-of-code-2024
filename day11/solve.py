import time
from functools import lru_cache

def load_data(file_path="input"):
    with open(file_path, 'r') as file:
        return [int(num) for num in file.read().strip().split()]

def split_stones(num):
    if num == 0:
        return [1]
    num_str = str(num)
    length = len(num_str)
    if length % 2 == 0:
        return [int(num_str[:length//2]), int(num_str[length//2:])]
    return [num * 2024]

@lru_cache(maxsize=None)
def calculate_splits(num, remaining_blinks):
    if remaining_blinks == 0:
        return 1
    return sum(calculate_splits(split, remaining_blinks - 1) for split in split_stones(num))

def part_one(numbers):
    start = time.time()
    total_stones = sum(calculate_splits(num, 25) for num in numbers)
    print(total_stones)
    print(f"Part 1 completed in {time.time() - start:.2f} seconds")

def part_two(numbers):
    start = time.time()
    total_stones = sum(calculate_splits(num, 75) for num in numbers)
    print(total_stones)
    print(f"Part 2 completed in {time.time() - start:.2f} seconds")

if __name__ == "__main__":
    initial_stones = load_data()
    part_one(initial_stones)
    part_two(initial_stones)