import Data.Bits
import Data.Char
import Data.List
import Data.Ord
import Numeric
import System.IO

-- Why isn't there an easy built in for this...
bitsToInt :: [Int] -> Int
bitsToInt = foldl' (\acc x -> acc * 2 + x) 0

-- Find the most common value in a string
mostCommonValue :: String -> Int
mostCommonValue x = digitToInt $ head $ maximumBy (comparing length) $ group $ sort x

-- Find a value using the algorithm from part 2.
findVal :: [String] -> (Int -> Int) -> [Int]
findVal [x] _ = map digitToInt x
findVal xs f = common : findVal (map tail $ filter (\x -> digitToInt (head x) == common) xs) f
  where
    common = f $ mostCommonValue $ head $ transpose xs

-- Get the gamma; epsilon is just the negation of gamma.
solution :: String -> Int
solution input =
  bitsToInt epsilon * bitsToInt gamma
  where
    gamma = map mostCommonValue $ transpose $ lines input
    epsilon = map (xor 1) gamma

-- Use the findVal helper to calculate both oxRate and scrub
solution2 :: String -> Int
solution2 input = scrub * oxRate
  where
    oxRate = bitsToInt $ findVal (lines input) id
    scrub = bitsToInt $ findVal (lines input) (xor 1)

-- A solution to part 1 that's probably too clever...
solution' :: String -> Int
solution' input = bitsToInt epsilon * bitsToInt gamma
  where
    gamma = map (fromEnum . (> breakEven)) $ foldl1 (zipWith (+)) $ map (map digitToInt) $ lines input
    epsilon = map (xor 1) gamma
    breakEven = length (lines input) `div` 2

main = do
  handle <- openFile "input.txt" ReadMode
  contents <- hGetContents handle
  print (solution contents)
  print (solution' contents)
  -- print (solution2 contents)
  hClose handle
