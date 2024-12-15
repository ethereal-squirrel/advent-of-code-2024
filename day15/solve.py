direction_map = {">": 1 + 0j, "<": -1 + 0j, "^": -1j, "v": 1j}

with open("input") as file:
    space_data, instructions = file.read().split("\n\n")


def part1():

    space_lines = space_data.split("\n")
    width, height = len(space_lines[0]), len(space_lines)

    space = {
        complex(x, y): space_lines[y][x] for y in range(height) for x in range(width)
    }
    robot_position = next(key for key in space if space[key] == "@")
    space[robot_position] = "."

    for direction in [direction_map[char] for char in instructions.replace("\n", "")]:
        if space[robot_position + direction] == ".":
            robot_position += direction
        elif space[robot_position + direction] == "O":
            count = 1
            while space[robot_position + count * direction] == "O":
                count += 1
            if space[robot_position + count * direction] == ".":
                space[robot_position + direction] = "."
                space[robot_position + count * direction] = "O"
                robot_position += direction

    result = sum(
        [
            100 * position.imag + position.real
            for position in space
            if space[position] == "O"
        ]
    )
    print(int(result))


def part2():
    space = [
        "".join(
            [char * 2 if char in ["#", ".", "@"] else "[]" for char in line]
        ).replace("@@", "@.")
        for line in space_data.split("\n")
    ]

    width, height = len(space[0]), len(space)
    space = {complex(x, y): space[y][x] for y in range(height) for x in range(width)}

    robot_position = [key for key in space if space[key] == "@"][0]
    space[robot_position] = "."

    for direction in [direction_map[char] for char in instructions.replace("\n", "")]:
        if space[robot_position + direction] == ".":
            robot_position += direction
        elif space[robot_position + direction] in ["[", "]"] and direction in [
            -1 + 0j,
            1 + 0j,
        ]:
            count = 1
            while space[robot_position + count * direction] in ["[", "]"]:
                count += 1
            if space[robot_position + count * direction] == ".":
                for i in range(count, 0, -1):
                    space[robot_position + i * direction] = space[
                        robot_position + (i - 1) * direction
                    ]
                robot_position += direction
        elif space[robot_position + direction] in ["[", "]"] and direction in [1j, -1j]:
            front = [
                z
                for z in [robot_position + direction, robot_position + direction - 1]
                if space[z] == "["
            ]
            seen = set(front)
            can_move = True
            while can_move and len(front) > 0:
                current = front.pop()
                can_move = (
                    space[current + direction] != "#"
                    and space[current + direction + 1 + 0j] != "#"
                )
                new_boxes = [
                    z
                    for z in [current + direction + complex(j, 0) for j in range(-1, 2)]
                    if space[z] == "["
                ]
                seen.update(new_boxes)
                front.extend(new_boxes)
            if can_move:
                for layer in range(
                    abs(
                        int(
                            min([-direction.imag * z.imag for z in seen])
                            - robot_position.imag
                        )
                    ),
                    0,
                    -1,
                ):
                    for z in [
                        w
                        for w in seen
                        if w.imag == (robot_position + layer * direction).imag
                    ]:
                        space[z] = "."
                        space[z + 1 + 0j] = "."
                        space[z + direction] = "["
                        space[z + direction + 1 + 0j] = "]"
                robot_position += direction

    print(int(sum([100 * z.imag + z.real for z in space if space[z] == "["])))


part1()
part2()
