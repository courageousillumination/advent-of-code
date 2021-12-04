import Data.List
import Data.List.Split (chunksOf, splitOn)
import Debug.Trace
import System.IO

type BingoBoard = [[Int]]

isWinner :: BingoBoard -> Bool
isWinner board = any (all (-1 ==)) board || any (all (-1 ==)) (transpose board)

markBoard :: Int -> BingoBoard -> BingoBoard
markBoard val board = [[z | x <- row, let z = if x /= val then x else -1] | row <- board]

scoreBoard :: BingoBoard -> Int -> Int
scoreBoard board val = val * sum (filter (-1 /=) $ concat board)

runSolution :: [BingoBoard] -> [Int] -> Int
runSolution boards (x : xs) = case winner of
  Nothing -> runSolution newBoards xs
  Just board -> scoreBoard board x
  where
    newBoards = map (markBoard x) boards
    winner = find isWinner newBoards
runSolution _ _ = undefined -- Should not happen

runSolution2 :: [BingoBoard] -> [Int] -> Int
runSolution2 boards (x : xs) = case winner of
  Nothing -> runSolution2 filteredBoards xs
  Just board -> if null filteredBoards then scoreBoard board x else runSolution2 filteredBoards xs
  where
    newBoards = map (markBoard x) boards
    winner = find isWinner newBoards
    filteredBoards = filter (not . isWinner) newBoards
runSolution2 _ _ = undefined -- Should not happen

solution :: [String] -> Int
solution input = runSolution2 boards nums
  where
    nums = map read $ splitOn "," $ head input
    boards = map (drop 1 . map (map read . words)) (chunksOf 6 $ drop 1 input)

main = do
  handle <- openFile "input.txt" ReadMode
  contents <- hGetContents handle
  print (solution $ lines contents)
  hClose handle
