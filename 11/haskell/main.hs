import Data.Array
import Data.Char
import Data.List
import Data.List.Split
import Data.Maybe
import System.IO

-- Uses haskell arrays because we're performing a bunch of index operations
type Position = (Int, Int)

type Grid = Array (Int, Int) Int

buildArray :: String -> Grid
buildArray value =
  array
    ((1, 1), (w, h))
    [ ((x, y), v)
      | (y, vs) <- zip [1 ..] vss,
        (x, v) <- zip [1 ..] vs
    ]
  where
    h = length vss
    w = length $ head vss
    vss = map (map digitToInt) $ lines value

prettyPrintGrid :: Grid -> String
prettyPrintGrid grid = foldr (\(x, y) acc -> (if y == 1 then "\n" else "") ++ show (grid ! (x, y)) ++ " " ++ acc) [] (indices grid)

validPosition :: ((Int, Int), (Int, Int)) -> Position -> Bool
validPosition ((minX, minY), (maxX, maxY)) (x, y) =
  x <= maxX && x >= minX && y <= maxY && y >= minY

getNeighbors :: ((Int, Int), (Int, Int)) -> Position -> [Position]
getNeighbors bounds (x, y) =
  filter
    (validPosition bounds)
    [(x + dx, y + dy) | dy <- [-1, 0, 1], dx <- [-1, 0, 1]]

incrementPositions :: Grid -> [Position] -> Grid
incrementPositions grid positions = grid // [(pos, grid ! pos + 1) | pos <- positions]

zeroPositions :: Grid -> [Position] -> Grid
zeroPositions grid positions = grid // [(pos, 0) | pos <- positions]

getFlashes :: Grid -> [Position]
getFlashes grid = foldl' (\acc x -> if grid ! x > 9 then x : acc else acc) [] $ indices grid

applyFlashes :: Grid -> [Position] -> (Grid, [Position])
applyFlashes grid flashed =
  if null flashes
    then (grid, flashed)
    else applyFlashes (foldl (\acc x -> incrementPositions acc [x]) grid (flashes >>= getNeighbors (bounds grid))) (flashes ++ flashed)
  where
    flashes = getFlashes grid \\ flashed

runGeneration :: Grid -> (Grid, Int)
runGeneration grid = (finalGrid, length flashes)
  where
    incremented = incrementPositions grid (indices grid)
    (flashed, flashes) = applyFlashes incremented []
    finalGrid = zeroPositions flashed flashes

runGenerations :: Grid -> Int -> Int
runGenerations _ 0 = 0
runGenerations grid i = flashes + runGenerations newGrid (i - 1)
  where
    (newGrid, flashes) = runGeneration grid

firstSync :: Grid -> Int -> Int
firstSync grid gen = if flashes == 100 then gen else firstSync newGrid gen + 1
  where
    (newGrid, flashes) = runGeneration grid

main = do
  handle <- openFile "input.txt" ReadMode
  contents <- hGetContents handle
  print (runGenerations (buildArray contents) 100)
  print (firstSync (buildArray contents) 1)
  hClose handle
