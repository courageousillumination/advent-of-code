import Data.Char
import Data.Either
import System.IO
import Text.ParserCombinators.Parsec

-- The state of the sub. This has 3 component, but the last is ignored in part 1
type SubState = (Int, Int, Int)

-- Commands that can be issued to the sub.
data Command = Forward Int | Up Int | Down Int deriving (Read, Show)

-- Pares a up/down/forward comand.
commandParser :: CharParser () Command
commandParser = command
  where
    command =
      Forward <$> (string "forward" >> commandValueParser)
        <|> Up <$> (string "up" >> commandValueParser)
        <|> Down <$> (string "down" >> commandValueParser)

-- Reads the operand for a command
commandValueParser :: CharParser () Int
commandValueParser = read <$> (spaces *> many1 digit)

-- Maps the raw input into a list of commands.
processInput :: String -> [Command]
processInput input = rights $ map (parse commandParser "Invalid Command") $ lines input

-- Part 1
strategy1 :: SubState -> Command -> SubState
strategy1 (x, y, aim) (Forward d) = (x + d, y, aim)
strategy1 (x, y, aim) (Up d) = (x, y - d, aim)
strategy1 (x, y, aim) (Down d) = (x, y + d, aim)

-- Part 2
strategy2 :: SubState -> Command -> SubState
strategy2 (x, y, aim) (Forward d) = (x + d, y + d * aim, aim)
strategy2 (x, y, aim) (Up d) = (x, y, aim - d)
strategy2 (x, y, aim) (Down d) = (x, y, aim + d)

-- Run the entire solution
solve :: String -> (SubState -> Command -> SubState) -> Int
solve input strategy = x * y
  where
    (x, y, _) = foldl strategy (0, 0, 0) $ processInput input

main = do
  handle <- openFile "input.txt" ReadMode
  contents <- hGetContents handle
  print (solve contents strategy1)
  print (solve contents strategy2)
  hClose handle
