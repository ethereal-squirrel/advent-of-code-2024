import re
import functools
import operator as op
import itertools as it
from collections.abc import Callable

def evaluate_expression(expression: str, operations: tuple[Callable]) -> int:
    target, *numbers = map(int, re.findall(r'\d+', expression))
    for operation_sequence in map(iter, it.product(operations, repeat=len(numbers) - 1)):
        apply_operation = lambda x, y: next(operation_sequence)(x, y)
        if functools.reduce(apply_operation, numbers) == target:
            return target
    return 0

def process_lines(input_lines: list[str]) -> None:
    concatenate = lambda x, y: int(f"{x}{y}")
    result_part1 = sum(evaluate_expression(line, (op.add, op.mul)) for line in input_lines)
    result_part2 = sum(evaluate_expression(line, (op.add, op.mul, concatenate)) for line in input_lines)
    print(result_part1, result_part2)

if __name__ == "__main__":
    with open('input') as file:
        process_lines(file.readlines())