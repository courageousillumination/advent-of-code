import Data.Function.Memoize
import Data.List
import Debug.Trace
import System.IO

type Position = (Int, Int)

type Amphipod = Char

type BoardState = [(Amphipod, Position)]

baseCost :: Amphipod -> Int
baseCost 'A' = 1
baseCost 'B' = 10
baseCost 'C' = 100
baseCost 'D' = 1000

-- Which column do we expect the ampihpods to be in?
targetColumn :: Amphipod -> Int
targetColumn 'A' = 3
targetColumn 'B' = 5
targetColumn 'C' = 7
targetColumn 'D' = 9

amphipodToChar :: Amphipod -> Char
amphipodToChar 'A' = 'A'
amphipodToChar 'B' = 'B'
amphipodToChar 'C' = 'C'
amphipodToChar 'D' = 'D'

-- Check if the board state is finished.
isFinished :: BoardState -> Bool
isFinished = all (\(a, (x, _)) -> targetColumn a == x)

getAmphipodAtPosition :: BoardState -> Position -> Amphipod
getAmphipodAtPosition board pos = case find (\(_, p) -> p == pos) board of
  Just (a, _) -> a
  _ -> error "Oh no"

getCharAtPosition :: BoardState -> Position -> Char
getCharAtPosition board pos = case find (\(_, p) -> p == pos) board of
  Just (a, _) -> amphipodToChar a
  _ -> '.'

prettyPrintBoard :: BoardState -> String
prettyPrintBoard board = unlines $ [row1, row2] ++ middleRows ++ [lastRow]
  where
    row1 = "#############"
    row2 = "#" ++ ([getCharAtPosition board (x, 1) | x <- [1 .. 11]]) ++ "#"
    middleRows =
      [ "###"
          ++ intersperse
            '#'
            [ getCharAtPosition board (x, y)
              | x <- [3, 5, 7, 9]
            ]
          ++ "###"
        | y <- [2, 3]
      ]
    lastRow = "  #########  "

-- X cost is computed by total distance traveled. Y cost is computed
-- by summing the two positions (this depends on the constrints of the
-- problem).
moveCost :: (Position, Position) -> Amphipod -> Int
moveCost ((x0, y0), (x1, y1)) a =
  (abs (x0 - x1) + (y0 -1) + (y1 -1)) * baseCost a

move :: BoardState -> (Position, Position) -> BoardState
move board (old, new) = sort $ (a, new) : filter (\(_, x) -> x /= old) board
  where
    a = case find (\(_, x) -> x == old) board of
      (Just (amph, _)) -> amph
      _ -> error "Bad move"

canMove :: BoardState -> (Position, Position) -> Bool
canMove board ((x0, y0), (x1, y1)) = not (interveningX || interveningY)
  where
    start = min x0 x1
    end = max x0 x1
    remainingPoints = filter ((/= (x0, y0)) . snd) board
    interveningX = any (\(_, (x, y)) -> y == 1 && x > start && x < end) remainingPoints
    interveningY = any (\(_, (x, y)) -> if x == x0 then y <= y0 else (x == x1) && (y <= y1)) remainingPoints

isInFinalPosition :: BoardState -> (Amphipod, Position) -> Bool
isInFinalPosition board (a, (x, y)) = xTarg && allFilled
  where
    xTarg = x == targetColumn a
    allFilled = all ((== a) . fst) $ filter (\(_, (x0, _)) -> x0 == x) board

getMovesPiece :: BoardState -> (Amphipod, Position) -> [(Position, Position)]
getMovesPiece board (a, (x, y))
  | y == 1 = if all ((== a) . fst) $ filter (\(_, (x0, _)) -> x0 == targetColumn a) board then filter (canMove board) [((x, y), (targetColumn a, 3)), ((x, y), (targetColumn a, 2))] else []
  | isInFinalPosition board (a, (x, y)) = []
  | otherwise = filter (canMove board) [((x, y), (x0, 1)) | x0 <- [1, 2, 4, 6, 8, 10, 11]]

getMoves :: BoardState -> [(Position, Position)]
getMoves board = concatMap (getMovesPiece board) board

-- This works, but needs memoization to actually function efficently...
optimalCost :: BoardState -> Int
optimalCost board
  | isFinished board = trace "done" 0
  | otherwise = cost
  where
    costs =
      map
        ( \m ->
            moveCost m (getAmphipodAtPosition board (fst m))
              + o1 (move board m)
        )
        $ getMoves board
    cost = if null costs then 1000000 else minimum costs

o1 = traceMemoize optimalCost

defaultBoard :: BoardState
defaultBoard =
  [ ('D', (3, 2)),
    ('D', (3, 3)),
    ('C', (5, 2)),
    ('C', (5, 3)),
    ('B', (9, 2)),
    ('B', (7, 3)),
    ('A', (7, 2)),
    ('A', (9, 3))
  ]

mostlySolved :: BoardState
mostlySolved =
  [ ('D', (9, 2)),
    ('D', (9, 3)),
    ('C', (7, 2)),
    ('C', (7, 3)),
    ('B', (3, 2)),
    ('B', (5, 3)),
    ('A', (3, 3)),
    ('A', (5, 2))
  ]

main =
  print
    ( o1 defaultBoard
    )
