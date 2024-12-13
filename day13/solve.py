from pathlib import Path
import re
from typing import Tuple, Generator

LARGE_ERROR = 10_000_000_000_000

def extract_coordinates(data):
    values = list(map(int, re.findall(r"\d+", data)))
    while values:
        yield ((values[0], values[1]), (values[2], values[3]), (values[4], values[5]))
        values = values[6:]

def find_minimum_cost(point_a, point_b, target):
    ax, ay = point_a
    bx, by = point_b
    tx, ty = target
    lowest_cost = float('inf')
    
    for b_count in range(1, 101):
        x_left = tx - (b_count * bx)
        y_left = ty - (b_count * by)
        
        if x_left < 0 or y_left < 0:
            break
        
        if x_left % ax == 0:
            a_count = x_left // ax
            if ay * a_count == y_left:
                lowest_cost = min(3 * a_count + b_count, lowest_cost)
    
    return 0 if lowest_cost == float('inf') else lowest_cost

def compute_part1(data: str) -> int:
    return sum(find_minimum_cost(point_a, point_b, target) for point_a, point_b, target in extract_coordinates(data))

def calculate_with_margin(point_a, point_b, target, margin):
    ax, ay = point_a
    bx, by = point_b
    tx, ty = target[0] + margin, target[1] + margin

    num = ax * bx * ty - ay * bx * tx
    denom = ax * by - ay * bx
    x_cross = num // denom
    b_count = x_cross // bx
    a_count = (tx - x_cross) // ax
    
    if (
        a_count >= 0
        and b_count >= 0
        and ay * a_count + by * b_count == ty
        and ax * a_count + bx * b_count == tx
    ):
        return b_count + 3 * a_count
    return 0

def compute_part2(data: str, margin: int = LARGE_ERROR) -> int:
    return sum(calculate_with_margin(point_a, point_b, target, margin) for point_a, point_b, target in extract_coordinates(data))


if __name__ == "__main__":
    data_input = Path("input").read_text()

    print(f"Part 1: {compute_part1(data_input)}")
    print(f"Part 2: {compute_part2(data_input)}")