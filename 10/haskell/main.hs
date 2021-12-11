import Data.Either
import Data.List
import System.IO

middleElement :: [Int] -> Int
middleElement xs = sort xs !! (length xs `div` 2)

isClosing :: Char -> Bool
isClosing x = x `elem` ">)}]"

isOpening :: Char -> Bool
isOpening x = x `elem` "<({["

getClosing :: Char -> Char
getClosing '<' = '>'
getClosing '(' = ')'
getClosing '{' = '}'
getClosing '[' = ']'
getClosing _ = error "Unknown closing character"

scoreError :: Char -> Int
scoreError ')' = 3
scoreError ']' = 57
scoreError '}' = 1197
scoreError '>' = 25137
scoreError _ = error "Unknown character"

scoreCompletionChar :: Char -> Int
scoreCompletionChar '(' = 1
scoreCompletionChar '[' = 2
scoreCompletionChar '{' = 3
scoreCompletionChar '<' = 4
scoreCompletionChar _ = error "Unknown character"

scoreCompletion :: String -> Int
scoreCompletion = foldl' (\acc x -> acc * 5 + scoreCompletionChar x) 0

processLineAcc :: String -> String -> Either Char String
processLineAcc acc [] = Right acc
processLineAcc acc (x : xs)
  | isOpening x = processLineAcc (x : acc) xs
  | not (null acc) && x == getClosing (head acc) = processLineAcc (tail acc) xs
  | otherwise = Left x

-- Returns an Either with the Left containing the char that failed (if corrupted)
-- or the Right containing expected closing characters
processLine :: String -> Either Char String
processLine = processLineAcc []

solution1 :: String -> Int
solution1 inp = sum $ map scoreError $ lefts $ map processLine $ lines inp

solution2 :: String -> Int
solution2 inp = middleElement $ map scoreCompletion $ rights $ map processLine $ lines inp

main = do
  handle <- openFile "input.txt" ReadMode
  contents <- hGetContents handle
  print (solution1 contents)
  print (solution2 contents)
  hClose handle
