import Data.Either
import Data.List
import Data.Map
import System.IO
import Text.ParserCombinators.Parsec

type BasePair = (Char, Char)

type PairCounter = Map BasePair Int

type RuleMapEntry = (BasePair, (BasePair, BasePair))

type RuleMap = Map BasePair (BasePair, BasePair)

data Day14Input = Day14Input String RuleMap deriving (Show)

stringToBasePairs :: String -> [BasePair]
stringToBasePairs (a : b : xs) = (a, b) : stringToBasePairs (b : xs)
stringToBasePairs _ = []

stringToPairCounter :: String -> PairCounter
stringToPairCounter input =
  fromList $
    Data.List.map (\x -> (head x, length x)) $
      group $ sort $ stringToBasePairs input

buildRuleMapEntry :: BasePair -> Char -> RuleMapEntry
buildRuleMapEntry (a, b) c = ((a, b), ((a, c), (c, b)))

day14 :: CharParser () Day14Input
day14 =
  Day14Input
    <$> template
    <*> (string "\n\n" >> rules)

template :: CharParser () String
template = many (noneOf "\n")

rules :: CharParser () RuleMap
rules = fromList <$> sepBy rule (char '\n')

rule :: CharParser () RuleMapEntry
rule = do
  a <- upper
  b <- upper
  string " -> "
  buildRuleMapEntry (a, b) <$> upper

incrementBy :: Int -> Maybe Int -> Maybe Int
incrementBy amount curr = case curr of
  Just y -> Just (amount + y)
  Nothing -> Just amount

applyRules :: PairCounter -> RuleMap -> PairCounter
applyRules pairs rules = Data.Map.foldrWithKey update empty pairs
  where
    update key x acc = case Data.Map.lookup key rules of
      Just (pair1, pair2) -> Data.Map.alter (incrementBy x) pair1 (Data.Map.alter (incrementBy x) pair2 acc)
      Nothing -> Data.Map.alter (incrementBy x) key acc

-- Note that this scoring won't count the last charater. So it needs to be passed
-- in explicitly.
score :: Char -> PairCounter -> Int
score lastChar pairs = Data.List.last sorted - Data.List.head sorted
  where
    sorted = sort $elems $ Data.Map.foldrWithKey update (fromList [(lastChar, 1)]) pairs
    update (a, _) x acc = Data.Map.alter (incrementBy x) a acc

solution1 (Day14Input template rules) =
  score (Data.List.last template) $ Data.List.foldl (\acc _ -> applyRules acc rules) (stringToPairCounter template) [1 .. 10]

solution2 (Day14Input template rules) =
  score (Data.List.last template) $ Data.List.foldl (\acc _ -> applyRules acc rules) (stringToPairCounter template) [1 .. 40]

main = do
  handle <- openFile "input.txt" ReadMode
  contents <- hGetContents handle
  let parsed = fromRight undefined $ parse day14 "Invalid input" contents
  print (solution1 parsed)
  print (solution2 parsed)
  hClose handle
