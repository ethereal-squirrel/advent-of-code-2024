lines = File.readlines('input').map(&:chomp)
Y = lines.size
X = lines[0].size
count = 0

(1...(Y - 1)).each do |y|
  (1...(X - 1)).each do |x|
    d1 = lines[y - 1][x - 1] + lines[y][x] + lines[y + 1][x + 1]
    d2 = lines[y + 1][x - 1] + lines[y][x] + lines[y - 1][x + 1]

    if (d1 == "MAS" || d1 == "SAM") && (d2 == "MAS" || d2 == "SAM")
      count += 1
    end
  end
end

puts count