from collections import deque

def read_input():
    with open("input") as f:
        lines = f.read().splitlines()
    return {(row, col): char 
            for row, line in enumerate(lines)
            for col, char in enumerate(line)}

def get_connected_region(start_pos, grid):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    target_value = grid[start_pos]
    region = set()
    boundary_count = 0
    queue = deque([start_pos])
    
    while queue:
        current = queue.popleft()
        if current in region:
            continue
            
        region.add(current)
        row, col = current
        
        for dy, dx in directions:
            next_pos = (row + dy, col + dx)
            if grid.get(next_pos) == target_value:
                queue.append(next_pos)
            else:
                boundary_count += 1
                
    return len(region), boundary_count, region

def calculate_corner_score(region):
    if not region:
        return 0
        
    rows = {r for r, _ in region}
    cols = {c for _, c in region}
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    
    corners = 0
    double_corners = 0
    
    for row in range(min_row, max_row + 2):
        for col in range(min_col, max_col + 2):
            cell_config = sum(
                ((row + y, col + x) in region) << i
                for i, (y, x) in enumerate([
                    (-1, -1), (-1, 0),
                    (0, -1), (0, 0)
                ])
            )
            
            if cell_config in [6, 9]:
                double_corners += 1
            elif cell_config not in [0, 3, 5, 10, 12, 15]:
                corners += 1
                
    return corners + double_corners

def solve():
    grid = read_input()
    processed = set()
    part1 = part2 = 0
    
    for position in grid:
        if position not in processed:
            size, boundary, region = get_connected_region(position, grid)
            processed.update(region)
            
            part1 += size * boundary
            part2 += size * calculate_corner_score(region)
    
    return part1, part2

if __name__ == "__main__":
    answer1, answer2 = solve()
    print(f"Part 1: {answer1}")
    print(f"Part 2: {answer2}")