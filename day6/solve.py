with open("input") as file:
    lines = file.read().split()
width, height = len(lines), len(lines[0])

distance = [
    [min(abs(x), abs(width - 1 - x), abs(y), abs(height - 1 - y)) for x in range(width)]
    for y in range(height)
]

for y in range(height):
    for x in range(width):
        if lines[y][x] == "^":
            start_position = (x, y)
        for k in range(height):
            if lines[y][k] == "#":
                distance[y][x] = min(distance[y][x], abs(k - x) - 1)
            if lines[k][x] == "#":
                distance[y][x] = min(distance[y][x], abs(k - y) - 1)

directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def navigate(obstacle_x, obstacle_y):
    heading = 0
    x, y = start_position
    visited_positions, visited_states = set(), set()
    visited_positions.add((x, y))
    visited_states.add((x, y, heading))
    
    while True:
        dx, dy = directions[heading]
        if obstacle_x and x != obstacle_x and y != obstacle_y:
            step = distance[y][x]
            while step >= 1:
                x += step * dx
                y += step * dy
                step = distance[y][x]
        
        next_x, next_y = x + dx, y + dy
        if next_x < 0 or next_x >= width or next_y < 0 or next_y >= height:
            return visited_positions, False
        if lines[next_y][next_x] == "#" or (next_x == obstacle_x and next_y == obstacle_y):
            heading = (heading + 1) % 4
        else:
            x, y = next_x, next_y
            if not obstacle_x:
                visited_positions.add((x, y))
            if (x, y, heading) in visited_states:
                return visited_positions, True
            visited_states.add((x, y, heading))

visited, _ = navigate(None, None)
part1_result = len(visited)
part2_result = sum(navigate(x, y)[1] for x, y in visited if (x, y) != start_position)

print(part1_result, part2_result)