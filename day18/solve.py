from collections import deque


def find_shortest_path(grid, start, destination):
    num_rows, num_cols = len(grid), len(grid[0])
    queue = deque([(start, [])])
    visited_nodes = {start}

    while queue:
        (current_row, current_col), current_path = queue.popleft()

        if (current_row, current_col) == destination:
            return current_path + [(current_row, current_col)]

        for delta_row, delta_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = current_row + delta_row, current_col + delta_col
            if (
                0 <= new_row < num_rows
                and 0 <= new_col < num_cols
                and grid[new_row][new_col] == 0
                and (new_row, new_col) not in visited_nodes
            ):
                queue.append(
                    ((new_row, new_col), current_path + [(current_row, current_col)])
                )
                visited_nodes.add((new_row, new_col))

    return None


with open("./input", "r") as file:
    obstacle_list = [line.strip() for line in file]

grid_dimension = 71
grid = [[0] * grid_dimension for _ in range(grid_dimension)]

total_obstacles = 1024
for index in range(total_obstacles):
    row, col = map(int, obstacle_list[index].split(","))
    grid[row][col] = 1

path_result = find_shortest_path(grid, (0, 0), (grid_dimension - 1, grid_dimension - 1))
print("Part 1:", len(path_result) - 1)

grid = [[0] * grid_dimension for _ in range(grid_dimension)]
for index, obstacle in enumerate(obstacle_list):
    row, col = map(int, obstacle.split(","))
    grid[row][col] = 1
    path_result = find_shortest_path(
        grid, (0, 0), (grid_dimension - 1, grid_dimension - 1)
    )

    if path_result is None:
        print("Part 2:", obstacle)
        break
