import Data.Either
import Data.List
import System.IO
import Text.ParserCombinators.Parsec

type Point = (Int, Int)

data Direction = Horizontal | Vertical deriving (Show, Eq)

data FoldInstruction = FoldInstruction Direction Int deriving (Show)

data Day13Input = Day13Input [Point] [FoldInstruction] deriving (Show)

day13 :: CharParser () Day13Input
day13 =
  Day13Input
    <$> endBy point (char '\n')
    <*> (char '\n' >> sepBy instruction (char '\n'))

instruction :: CharParser () FoldInstruction
instruction =
  FoldInstruction
    <$> (string "fold along " >> direction)
    <*> (char '=' >> number)

direction :: CharParser () Direction
direction =
  Horizontal <$ char 'x'
    <|> Vertical <$ char 'y'

point :: CharParser () Point
point = (,) <$> number <*> (char ',' >> number)

number :: CharParser () Int
number = read <$> many1 digit

applyInstruction :: FoldInstruction -> [Point] -> [Point]
applyInstruction (FoldInstruction Horizontal at) =
  nub . map (\(x, y) -> (at - abs (at - x), y))
applyInstruction (FoldInstruction Vertical at) =
  nub . map (\(x, y) -> (x, at - abs (at - y)))

solution1 :: Day13Input -> Int
solution1 (Day13Input points instructions) =
  length $ applyInstruction (head instructions) points

prettyPrintPoints :: [Point] -> String
prettyPrintPoints points =
  [ if x == maxX + 1 then '\n' else if (x, y) `elem` points then '#' else '.'
    | y <- [0 .. maxY],
      x <- [0 .. maxX + 1]
  ]
  where
    maxX = maximum $ map fst points
    maxY = maximum $ map snd points

solution2 :: Day13Input -> String
solution2 (Day13Input points instructions) =
  prettyPrintPoints $ foldl (flip applyInstruction) points instructions

main = do
  handle <- openFile "input.txt" ReadMode
  contents <- hGetContents handle
  let parsed = fromRight (Day13Input [] []) $ parse day13 "Invalid input" contents
  print (solution1 parsed)
  putStrLn (solution2 parsed)
  hClose handle
