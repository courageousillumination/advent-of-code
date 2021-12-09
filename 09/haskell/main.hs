import Data.Array
import Data.Char
import Data.List
import Data.Maybe
import System.IO

type Size = (Int, Int)

type Position = (Int, Int)

-- Uses haskell arrays because we're performing a bunch of index operations
type Board = Array (Int, Int) Int

buildArray :: String -> Board
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

isLowPoint :: Board -> Position -> Bool
isLowPoint board (x, y) = all ((> value) . (board !)) neighbors
  where
    value = board ! (x, y)
    neighbors = getNeighbors (bounds board) (x, y)

getNeighbors :: ((Int, Int), (Int, Int)) -> Position -> [Position]
getNeighbors ((minX, minY), (maxX, maxY)) (x, y) = catMaybes [left, right, up, down]
  where
    left = if x == minX then Nothing else Just (x -1, y)
    right = if x == maxX then Nothing else Just (x + 1, y)
    up = if y == minY then Nothing else Just (x, y - 1)
    down = if y == maxY then Nothing else Just (x, y + 1)

getBasin :: Board -> Position -> [Position]
getBasin board position =
  if board ! position == 9
    then []
    else position : concatMap (getBasin board) heigherNeighbors
  where
    value = board ! position
    neighbors = getNeighbors (bounds board) position
    heigherNeighbors = filter ((> value) . (board !)) neighbors

getBasinSize :: Board -> Position -> Int
getBasinSize board position = length $ nub $ getBasin board position

solution1 :: String -> Int
solution1 value = foldl foldFunc 0 $ indices board
  where
    board = buildArray value
    foldFunc acc x = if isLowPoint board x then board ! x + acc + 1 else acc

solution2 :: String -> Int
solution2 value = product $ take 3 $ reverse $ sort $ map (getBasinSize board) lowPoints
  where
    board = buildArray value
    lowPoints = filter (isLowPoint board) (indices board)

main = do
  handle <- openFile "input.txt" ReadMode
  contents <- hGetContents handle
  print (solution1 contents)
  print (solution2 contents)
  hClose handle
