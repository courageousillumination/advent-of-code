import Data.List
import Data.List.Split
import Data.Map
import System.IO

runGeneration :: Map Int Int -> Map Int Int
runGeneration xs = mapWithKey update xs
  where
    update 8 _ = xs ! 0
    update 6 _ = xs ! 7 + xs ! 0
    update k _ = xs ! (k + 1)

runGeneration' :: [Int] -> [Int]
runGeneration' [x0, x1, x2, x3, x4, x5, x6, x7, x8] = [x1, x2, x3, x4, x5, x6, x7 + x0, x8, x0]
runGeneration' _ = undefined

getNums :: String -> [Int]
getNums i = read <$> splitOn "," i

emptyMap = fromList $ zip [0 .. 8] (repeat 0)

-- getStarting :: String -> Map Int Int
getStarting input = Data.List.map (\x -> length $ Data.List.filter (== x) nums) [0 .. 8]
  where
    nums = getNums input

-- solution :: String -> [Int]
-- solution input = Data.Map.foldl (+) 0 $ Data.List.foldl (\acc _ -> runGeneration acc) (Data.Map.union (getStarting input) emptyMap) [1 .. 256]

solution input = sum $ Data.List.foldl (\acc _ -> runGeneration' acc) (getStarting input) [1 .. 256]

main = do
  handle <- openFile "input.txt" ReadMode
  contents <- hGetContents handle
  print (solution contents)
  hClose handle
