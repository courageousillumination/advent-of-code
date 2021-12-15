import Data.Array as A (Array, array, bounds, indices, (!))
import Data.Char (digitToInt)
import Data.Foldable (minimumBy)
import Data.List as L (delete, foldl', map, minimumBy)
import Data.Map as M (Map, fromList, insert, (!))
import Data.Maybe (catMaybes)
import Data.Ord (comparing)
import System.IO
  ( IOMode (ReadMode),
    hClose,
    hGetContents,
    openFile,
  )

type Position = (Int, Int)

type Grid = Array Position Int

buildArrayInts :: [[Int]] -> Grid
buildArrayInts value =
  array
    ((1, 1), (w, h))
    [ ((x, y), v)
      | (y, vs) <- zip [1 ..] vss,
        (x, v) <- zip [1 ..] vs
    ]
  where
    h = length vss
    w = length $ head vss
    vss = value

buildArray :: String -> Grid
buildArray value = buildArrayInts $ L.map (L.map digitToInt) $ lines value

getNeighbors :: ((Int, Int), (Int, Int)) -> Position -> [Position]
getNeighbors ((minX, minY), (maxX, maxY)) (x, y) = catMaybes [left, right, up, down]
  where
    left = if x == minX then Nothing else Just (x -1, y)
    right = if x == maxX then Nothing else Just (x + 1, y)
    up = if y == minY then Nothing else Just (x, y - 1)
    down = if y == maxY then Nothing else Just (x, y + 1)

-- We'll use Dijkstra's here.
dijkstra :: [Position] -> Grid -> Map Position Int -> Map Position Int
dijkstra [] grid distances = distances -- Base case, we've dealt with all distances.
dijkstra points grid distances = dijkstra remaining grid newDistances
  where
    -- minimumBy is O(n^2) so this will take forever. Maybe need a priority queue?
    u = minimumBy (comparing (distances M.!)) points
    distU = distances M.! u
    remaining = L.delete u points
    newDistances = L.foldl' update distances (getNeighbors (bounds grid) u)
    update acc pos =
      if (distU + grid A.! pos) < (distances M.! pos)
        then M.insert pos (distU + grid A.! pos) acc
        else acc

solution :: Grid -> Int
solution grid = dijkstra (A.indices grid) grid distances M.! snd (bounds grid)
  where
    distances = M.fromList (((1, 1), 0) : [(x, maxBound :: Int) | x <- A.indices grid, x /= (1, 1)])

cycleValue :: Char -> Int -> Int -> Int
cycleValue x i j = if val >= 10 then (val `mod` 10) + 1 else val
  where
    val = digitToInt x + i + j

generateTiledGrid :: String -> [[Int]]
generateTiledGrid input =
  [[cycleValue x i j | j <- [0 .. 4], x <- row] | i <- [0 .. 4], row <- l]
  where
    l = lines input

main = do
  handle <- openFile "input.txt" ReadMode
  contents <- hGetContents handle
  print (solution $ buildArray contents)
  print (solution $ buildArrayInts $ generateTiledGrid contents)
  hClose handle
