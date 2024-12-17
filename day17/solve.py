from pathlib import Path
from operator import xor
import time

def get_operand_value(operand, reg_a, reg_b, reg_c):
    if operand in (4, 5, 6):
        return [reg_a, reg_b, reg_c][operand - 4]
    elif operand == 7:
        raise RuntimeError("Reserved operand")
    return operand

def run_program(program, reg_a, reg_b, reg_c):
    pc, output = 0, []
    while pc < len(program):
        instr, operand = program[pc], program[pc + 1]
        pc += 2
        if instr == 0:
            reg_a //= (1 << get_operand_value(operand, reg_a, reg_b, reg_c))
        elif instr == 1:
            reg_b = xor(reg_b, operand)
        elif instr == 2:
            reg_b = get_operand_value(operand, reg_a, reg_b, reg_c) % 8
        elif instr == 3 and reg_a != 0:
            pc = operand
        elif instr == 4:
            reg_b = xor(reg_b, reg_c)
        elif instr == 5:
            output.append(get_operand_value(operand, reg_a, reg_b, reg_c) % 8)
        elif instr in (6, 7):
            reg = reg_a // (1 << get_operand_value(operand, reg_a, reg_b, reg_c))
            if instr == 6:
                reg_b = reg
            else:
                reg_c = reg
    return output

def parse_input(input_data):
    lines = input_data.splitlines()
    reg_a, reg_b, reg_c = (int(lines[i].split(":")[1].strip()) for i in range(3))
    program = list(map(int, lines[4].split(":")[1].strip().split(",")))
    return reg_a, reg_b, reg_c, program

def part1(input_data):
    reg_a, reg_b, reg_c, program = parse_input(input_data)
    return run_program(program, reg_a, reg_b, reg_c)

def find_solution(program, reg_a, required_output):
    reg_a *= 8
    for n in range(8):
        if run_program(program, reg_a + n, 0, 0) == required_output:
            yield reg_a + n

def part2(input_data):
    reg_a, reg_b, reg_c, program = parse_input(input_data)
    required_output, reg_a_options = [], {0}

    for value in reversed(program):
        required_output.insert(0, value)
        reg_a_options = {a for reg_a in reg_a_options for a in find_solution(program, reg_a, required_output)}

    return min(reg_a_options)

if __name__ == "__main__":
    start_time = time.time()
    input_data = Path("input").read_text()
    print("Part 1:", part1(input_data))
    print("Part 2:", part2(input_data))
    print(f"Time taken: {time.time() - start_time:.2f} seconds")