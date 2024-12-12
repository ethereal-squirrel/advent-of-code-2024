// https://adventofcode.com/2024/day/6

import fs from "fs";
const originalMap: string[] = [];

fs.readFileSync("./input", "utf8")
  .split("\n")
  .map((line) => {
    originalMap.push(line);
  });

const mapHeight = originalMap.length;
const mapWidth = originalMap[0].length;

enum Dir {
  Up = "up",
  Down = "down",
  Left = "left",
  Right = "right",
}

type Position = {
  y: number;
  x: number;
};

const coordToString = (y: number, x: number): string => `${y},${x}`;
const stringToCoord = (s: string): Position => {
  const [y, x] = s.split(",").map(Number);
  return { y, x };
};

const nextPosition: Record<Dir, (pos: Position) => Position> = {
  [Dir.Up]: (pos) => ({ y: pos.y - 1, x: pos.x }),
  [Dir.Down]: (pos) => ({ y: pos.y + 1, x: pos.x }),
  [Dir.Left]: (pos) => ({ y: pos.y, x: pos.x - 1 }),
  [Dir.Right]: (pos) => ({ y: pos.y, x: pos.x + 1 }),
};

const isValidPosition = (pos: Position): boolean => {
  return pos.y >= 0 && pos.y < mapHeight && pos.x >= 0 && pos.x < mapWidth;
};

const findStartPoint = (): [number, number] => {
  return originalMap
    .map((line, index) => {
      if (line.indexOf("^") !== -1) {
        return [index, line.indexOf("^")];
      }
    })
    .filter((each) => each !== undefined)[0] as [number, number];
};

const runMaze = (map: string[]) => {
  const visited = new Map<string, Set<Dir>>();
  let currentDirection = Dir.Up;
  const currentPosition: Position = {
    y: findStartPoint()[0],
    x: findStartPoint()[1],
  };

  const addVisit = (pos: Position, dir: Dir) => {
    const key = coordToString(pos.y, pos.x);
    const directions = visited.get(key) || new Set();
    if (directions.has(dir)) return false;
    directions.add(dir);
    visited.set(key, directions);
    return true;
  };

  addVisit(currentPosition, Dir.Up);

  while (true) {
    const nextPos = nextPosition[currentDirection](currentPosition);

    if (!isValidPosition(nextPos)) break;

    if (map[nextPos.y][nextPos.x] !== "#") {
      if (!addVisit(nextPos, currentDirection)) return null;
      currentPosition.y = nextPos.y;
      currentPosition.x = nextPos.x;
    } else {
      currentDirection = {
        [Dir.Up]: Dir.Right,
        [Dir.Right]: Dir.Down,
        [Dir.Down]: Dir.Left,
        [Dir.Left]: Dir.Up,
      }[currentDirection];
    }
  }

  return visited;
};

const partOne = async () => {
  const uniqueVisited = new Set<string>();
  const mazeResult = runMaze(originalMap);
  if (mazeResult !== null) {
    mazeResult.forEach((_, coord) => uniqueVisited.add(coord));
  }
  return uniqueVisited.size;
};

const partTwo = async () => {
  const initialRun = runMaze(originalMap);
  if (!initialRun) return "Invalid map input";

  const visitedPositions = [...initialRun.keys()]
    .map(stringToCoord)
    .filter((_, i) => i !== 0);

  const mapCache = new Map<string, string[]>();

  return visitedPositions.reduce((count, pos) => {
    const cacheKey = coordToString(pos.y, pos.x);
    let testMap = mapCache.get(cacheKey);

    if (!testMap) {
      testMap = originalMap.map((row) => row.slice());
      testMap[pos.y] =
        testMap[pos.y].slice(0, pos.x) + "#" + testMap[pos.y].slice(pos.x + 1);
      mapCache.set(cacheKey, testMap);
    }

    return count + (runMaze(testMap) === null ? 1 : 0);
  }, 0);
};

(function results() {
  const start = new Date();

  partOne().then((result) => {
    console.log("Running with small sample data due to time complexity");
    console.log("Day 6 part 1 result: ", result);
  });
  partTwo().then((result) => {
    console.log("Day 6 part 2 result: ", result, "\n");
  });

  const end = new Date();
  console.log(`Time taken: ${end.getTime() - start.getTime()}ms`);
})();
