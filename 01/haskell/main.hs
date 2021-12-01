import System.IO

-- Part 1
increasingDepth :: [Int] -> Int
increasingDepth (a : xs@(b : _))
  | b > a = 1 + increasingDepth xs
  | otherwise = increasingDepth xs
increasingDepth _ = 0

-- A version for part 1 using only list primitives
increasingDepth' :: [Int] -> Int
increasingDepth' xs = length $ filter id $ zipWith (>) (tail xs) xs

-- Part 2
windowIncreasingDepth :: [Int] -> Int
windowIncreasingDepth (a : xs@(b : c : d : _))
  | d > a = 1 + windowIncreasingDepth xs
  | otherwise = windowIncreasingDepth xs
windowIncreasingDepth _ = 0

-- Scaffolding
solution :: String -> Int
solution input =
  let depths = (map read $ lines input) :: [Int]
   in increasingDepth' depths

main = do
  handle <- openFile "input.txt" ReadMode
  contents <- hGetContents handle
  print (solution contents)
  hClose handle
