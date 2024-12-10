import System.IO
import Data.List
import qualified Data.Set as Set
import Data.Maybe (fromMaybe)
import Data.Time.Clock

type Coord = (Int, Int)
type Graph = [(Coord, [Coord])]

parseHeightmap :: FilePath -> IO [(Coord, Int)]
parseHeightmap filename = do
    content <- readFile filename
    return [ ((i, j), read [value])
           | (i, line) <- zip [0..] (lines content)
           , (j, value) <- zip [0..] line
           ]

createGraph :: [(Coord, Int)] -> Graph
createGraph heightmap = 
    [ (pos, [ (x + dx, y + dy) 
            | (dx, dy) <- possibleMoves
            , let newPos = (x + dx, y + dy)
            , lookup newPos heightmap == Just (height + 1)
            ])
    | (pos@(x, y), height) <- heightmap
    ]
  where
    possibleMoves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

dfs :: Graph -> Coord -> Coord -> Set.Set Coord -> Int
dfs graph start end visited
    | start == end = 1
    | otherwise = sum [ dfs graph neighbor end (Set.insert start visited)
                      | neighbor <- neighbors
                      , Set.notMember neighbor visited
                      ]
  where
    neighbors = fromMaybe [] (lookup start graph)

calculateResults :: Graph -> [Coord] -> [Coord] -> (Int, Int)
calculateResults graph starts ends = (pathExists, pathCount)
  where
    pathCount = sum [ dfs graph start end Set.empty | start <- starts, end <- ends ]
    pathExists = length [ () | start <- starts, end <- ends, dfs graph start end Set.empty > 0 ]

main :: IO ()
main = do
    start <- getCurrentTime
    heightmap <- parseHeightmap "input"
    let graph = createGraph heightmap
    let starts = [pos | (pos, height) <- heightmap, height == 0]
    let ends = [pos | (pos, height) <- heightmap, height == 9]
    let (pathExists, pathCount) = calculateResults graph starts ends
    putStrLn $ "Part 1: " ++ show pathExists
    putStrLn $ "Part 2: " ++ show pathCount
    finish <- getCurrentTime
    putStrLn $ "Total time: " ++ show (diffUTCTime finish start)