-- Part 1 is just the mid point of the list. That makes sense from a math perspective

import Data.List
import Data.List.Split
import System.IO

getPositions :: String -> [Int]
getPositions i = read <$> splitOn "," i

getTotalCost :: [Int] -> Int -> Int
getTotalCost positions target = sum $ map (abs . (target -)) positions

getTotalCost' :: [Int] -> Int -> Int
getTotalCost' positions target = sum $ map (triangle . abs . (target -)) positions

triangle :: Int -> Int
triangle n = (n * (n + 1)) `div` 2

-- Brute force part 1
part1 :: [Int] -> Int
part1 positions = minimum $ map (getTotalCost positions) [minimum positions .. maximum positions]

-- Part 1 using median
part1' :: [Int] -> Int
part1' positions = getTotalCost positions (sort positions !! (length positions `div` 2))

-- Brute force part 2
part2 :: [Int] -> Int
part2 positions = minimum $ map (getTotalCost' positions) [minimum positions .. maximum positions]

-- Part 2 using mean (I don't really know why this is... would need to do some reading)
part2' :: [Int] -> Int
part2' positions = getTotalCost' positions $ sum positions `div` length positions

main = do
  handle <- openFile "input.txt" ReadMode
  contents <- hGetContents handle
  print (part1' $ getPositions contents)
  print (part2' $ getPositions contents)
  hClose handle
