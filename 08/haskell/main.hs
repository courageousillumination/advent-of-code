import Data.List
import Data.List.Split
import Data.Maybe
import System.IO

type Mapping = [(Char, Char)]

codeToInt :: String -> Maybe Int
codeToInt "abcdefg" = Just 8
codeToInt "abdfg" = Just 5
codeToInt "acdeg" = Just 2
codeToInt "acdfg" = Just 3
codeToInt "acf" = Just 7
codeToInt "abcdfg" = Just 9
codeToInt "abdefg" = Just 6
codeToInt "bcdf" = Just 4
codeToInt "abcefg" = Just 0
codeToInt "cf" = Just 1
codeToInt _ = Nothing

allMappings :: [Mapping]
allMappings = map (zip ['a' .. 'g']) $ permutations ['a' .. 'g']

generateMapping :: [String] -> Maybe Mapping
generateMapping xs = do
  x1 <- find ((== 2) . length) xs
  x4 <- find ((== 4) . length) xs
  x7 <- find ((== 3) . length) xs
  x8 <- find ((== 7) . length) xs
  a <- find (`notElem` x4) x7
  b <- find (\x -> notElem x x7 && countOccurances x == 6) x4
  d <- find (\x -> notElem x x7 && countOccurances x /= 6) x4
  f <- find ((== 9) . countOccurances) x4
  c <- find (/= f) x1
  e <- find ((== 4) . countOccurances) x8
  g <- find (\x -> x /= d && countOccurances x == 7) x8
  return [('a', a), ('b', b), ('c', c), ('d', d), ('e', e), ('f', f), ('g', g)]
  where
    countOccurances x = length $ filter (elem x) xs

applyMapping :: Mapping -> Char -> Char
applyMapping [] _ = error "Can not find mapping"
applyMapping ((mapped, x) : xs) char = if x == char then mapped else applyMapping xs char

applyMappingStr :: Mapping -> String -> String
applyMappingStr mapping str = sort $ map (applyMapping mapping) str

-- Checks if a mapping is valid. Works by appling and then running codeToInt and checking for any failures
-- TODO: Monads maybe?
checkValidMapping :: Mapping -> [String] -> Bool
checkValidMapping mapping = all (isJust . (codeToInt . applyMappingStr mapping))

-- Convert [1,2,3] to 123
asInt :: [Int] -> Int
asInt = read . concatMap show

-- Process a single row.
-- Warning: This is a brute force solution and kind of slow
processRow :: [String] -> [String] -> Int
processRow left right = asInt $ map (fromJust . codeToInt . applyMappingStr validMap) right
  where
    validMap = fromJust $ find (`checkValidMapping` left) allMappings

processRow' :: [String] -> [String] -> Int
processRow' left right = asInt $ map (fromJust . codeToInt . applyMappingStr validMap) right
  where
    validMap = fromJust $ generateMapping left

-- Process the whole solution
solution :: String -> Int
solution text = sum $ map handleRow $ lines text

handleRow :: String -> Int
handleRow t = processRow' left right
  where
    left = splitOn " " $ head $ splitOn " | " t
    right = splitOn " " $ head $ tail $ splitOn " | " t

main = do
  handle <- openFile "input.txt" ReadMode
  contents <- hGetContents handle
  print (solution contents)
  hClose handle
