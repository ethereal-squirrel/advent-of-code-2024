def count_xmas(grid)
  directions = [
    [0, 1],
    [1, 0],
    [1, 1],
    [1, -1],
    [0, -1],
    [-1, 0],
    [-1, -1],
    [-1, 1]
  ]

  count = 0
  rows = grid.length
  cols = grid[0].length

  for r in 0...rows
    for c in 0...cols
      if grid[r][c] == 'X'
        directions.each do |dr, dc|
          found = true

          "XMAS".chars.each_with_index do |char, index|
            nr, nc = r + dr * index, c + dc * index

            if nr < 0 || nr >= rows || nc < 0 || nc >= cols || grid[nr][nc] != char
              found = false
              break
            end
          end

          count += 1 if found
        end
      end
    end
  end

  count
end

input = File.readlines('input').map(&:strip)

grid = input.map { |line| line.chars }

result = count_xmas(grid)

puts result