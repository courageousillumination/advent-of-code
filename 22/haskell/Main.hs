import Control.Arrow
import Control.Monad
import Data.Bifunctor
import Data.Either
import Data.List
import Data.Map (valid)
import Data.Maybe
import Debug.Trace
import System.IO
import Text.ParserCombinators.Parsec

type Range = (Int, Int)

type Prism = (Range, Range, Range)

data Command = On | Off deriving (Show)

data Instruction = Instruction Command Prism deriving (Show)

validRange :: Range -> Bool
validRange (a, b) = a <= b

validPrism :: Prism -> Bool
validPrism (x, y, z) = all validRange [x, y, z]

splitPrism :: Prism -> Prism -> [Prism]
splitPrism
  ((x10, x11), (y10, y11), (z10, z11))
  ((x00, x01), (y00, y01), (z00, z01)) = if hasIntersection then res else [((x00, x01), (y00, y01), (z00, z01))]
    where
      hasIntersection =
        x10 <= x01 && x11 >= x00
          && y10 <= y01
          && y11 >= y00
          && z10 <= z01
          && z11 >= z00
      xrange = (max x00 x10, min x01 x11)
      yrange = (max y00 y10, min y01 y11)
      p1 = ((x00, x10 - 1), (y00, y01), (z00, z01))
      p2 = ((x11 + 1, x01), (y00, y01), (z00, z01))
      p3 = (xrange, (y00, y10 - 1), (z00, z01))
      p4 = (xrange, (y11 + 1, y01), (z00, z01))
      p5 = (xrange, yrange, (z00, z10 - 1))
      p6 = (xrange, yrange, (z11 + 1, z01))
      res = filter validPrism [p1, p2, p3, p4, p5, p6]

applyInstruction :: [Prism] -> Instruction -> [Prism]
applyInstruction prisms (Instruction command prism) =
  case command of
    On -> prism : newPrisms
    _ -> newPrisms
  where
    newPrisms = concatMap (splitPrism prism) prisms

applyInstructions :: [Instruction] -> [Prism]
applyInstructions = foldl' applyInstruction []

volume :: Prism -> Int
volume ((x0, x1), (y0, y1), (z0, z1)) = (x1 - x0 + 1) * (y1 - y0 + 1) * (z1 - z0 + 1)

countOn :: [Prism] -> Int
countOn = sum . map volume

parseInstructions :: String -> [Instruction]
parseInstructions = map parseInstruction . lines

parseInstruction :: String -> Instruction
parseInstruction input = fromRight undefined instructions
  where
    instructions = parse instruction "(unknown)" input

instruction :: CharParser () Instruction
instruction = Instruction <$> command <*> (char ' ' *> prism)

prism :: CharParser () Prism
prism = toPrism <$> sepBy numberRange (char ',')

toPrism :: [Range] -> Prism
toPrism [x, y, z] = (x, y, z)
toPrism _ = error "Bad prism"

command :: CharParser () Command
command =
  choice
    [ string "on" >> return On,
      string "ff" >> return Off
    ]

numberRange :: CharParser () Range
numberRange =
  (,) <$> (anyChar *> char '=' *> number)
    <*> (string ".." *> number)

number :: CharParser () Int
number = ap sign nat

nat :: CharParser () Int
nat = read <$> many1 digit

sign :: CharParser () (Int -> Int)
sign = (char '-' >> return negate) <|> (optional (char '+') >> return id)

solution :: String -> Int
solution = countOn . applyInstructions . parseInstructions

main = do
  handle <- openFile "input.txt" ReadMode
  contents <- hGetContents handle
  print (solution contents)
  print (length $ applyInstructions $ parseInstructions $ contents)
  hClose handle
