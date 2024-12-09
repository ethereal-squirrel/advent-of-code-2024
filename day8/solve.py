from collections import defaultdict

def extract_transmitters(matrix):
    transmitters = defaultdict(list)

    for r_idx, row in enumerate(matrix):
        for c_idx, symbol in enumerate(row):
            if symbol != ".":
                transmitters[symbol].append((r_idx, c_idx))

    return transmitters

def is_within_bounds(position, total_rows, total_cols):
    return 0 <= position[0] < total_rows and 0 <= position[1] < total_cols

def execute():
    with open("input", "rt") as file:
        matrix = [line.strip() for line in file]
        total_rows, total_cols = len(matrix), len(matrix[0])

    transmitters = extract_transmitters(matrix)
    nodes_set1 = set()
    nodes_set2 = set()

    for coords in transmitters.values():
        if len(coords) == 1:
            continue

        for idx1 in range(len(coords) - 1):
            coord1 = coords[idx1]

            for idx2 in range(idx1 + 1, len(coords)):
                coord2 = coords[idx2]
                row_delta, col_delta = coord2[0] - coord1[0], coord2[1] - coord1[1]

                nodes_set2.add(coord1)
                nodes_set2.add(coord2)

                node = (coord1[0] - row_delta, coord1[1] - col_delta)
                if is_within_bounds(node, total_rows, total_cols):
                    nodes_set1.add(node)
                    while is_within_bounds(
                        node := (node[0] - row_delta, node[1] - col_delta),
                        total_rows,
                        total_cols,
                    ):
                        nodes_set2.add(node)

                node = (coord2[0] + row_delta, coord2[1] + col_delta)
                if is_within_bounds(node, total_rows, total_cols):
                    nodes_set1.add(node)
                    while is_within_bounds(
                        node := (node[0] + row_delta, node[1] + col_delta),
                        total_rows,
                        total_cols,
                    ):
                        nodes_set2.add(node)

    print(f"Part 1: {len(nodes_set1)}")
    print(f"Part 2: {len(nodes_set1 | nodes_set2)}")

if __name__ == "__main__":
    execute()