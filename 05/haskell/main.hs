-- The core algorithm here involves generating all points and then running some manipulation over them.
-- This takes a ton of memory and won't scale. We might want to think of another algorithm that scales.
import Data.Either
import Data.List
import System.IO
import Text.ParserCombinators.Parsec

-- Data types
type Point = (Int, Int)

data Line = Line Point Point deriving (Show, Eq)

-- BEGIN PARSING CODE --

lineParser :: CharParser () Main.Line
lineParser = toLine <$> sepBy pointParser (string " -> ")

pointParser :: CharParser () Point
pointParser = toPoint <$> sepBy number (char ',')

number :: CharParser () Int
number = read <$> many1 digit

toPoint :: [Int] -> Point
toPoint [x, y] = (x, y)
toPoint _ = error "Invalid point"

toLine :: [Point] -> Main.Line
toLine [p1, p2] = Line p1 p2
toLine _ = error "Invalid line"

processInput :: String -> [Main.Line]
processInput input = rights $ map (parse lineParser "Invalid Command") $ lines input

-- END PARSING CODE --

sign :: Int -> Int
sign x
  | x < 0 = -1
  | x > 0 = 1
  | otherwise = 0

generatePoints :: Main.Line -> [Point]
generatePoints (Main.Line (x1, y1) (x2, y2)) = [(x1 + d * xDir, y1 + d * yDir) | d <- [0 .. lineLength]]
  where
    dX = x2 - x1
    dY = y2 - y1
    xDir = sign dX
    yDir = sign dY
    lineLength = max (abs dX) (abs dY)

nonDiagonal :: Main.Line -> Bool
nonDiagonal (Main.Line (x1, y1) (x2, y2)) = x1 == x2 || y1 == y2

solution i = (length . filter ((> 1) . length) . group . sort) $ filter nonDiagonal (processInput i) >>= generatePoints

solution2 i = (length . filter ((> 1) . length) . group . sort) $ processInput i >>= generatePoints

main = do
  handle <- openFile "input.txt" ReadMode
  contents <- hGetContents handle
  print (solution2 contents)
  hClose handle
