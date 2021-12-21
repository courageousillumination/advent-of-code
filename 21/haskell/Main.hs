import Control.Arrow
import Data.Bifunctor
import Data.List
import Data.Maybe
import Debug.Trace
import System.IO

winningScore = 21

type Position = Int

type Score = Int

data Player = Player Position Score deriving (Show, Eq)

type DiceState = (Int, Int)

data Game = Game Player Player Int DiceState deriving (Show)

getWinner :: Game -> Maybe (Player, Player)
getWinner (Game p1@(Player _ score1) p2@(Player _ score2) _ _)
  | score1 >= winningScore = Just (p1, p2)
  | score2 >= winningScore = Just (p2, p1)
  | otherwise = Nothing

hasWinner :: Game -> Bool
hasWinner = isJust . getWinner

getDiceRollCount :: Game -> Int
getDiceRollCount (Game _ _ _ (_, count)) = count

moveAndScorePlayer :: Player -> Int -> Player
moveAndScorePlayer (Player pos score) amount = Player newPos (score + newPos + 1)
  where
    newPos = (pos + amount) `mod` 10

getDeterminsticDiceRoll :: DiceState -> (Int, DiceState)
getDeterminsticDiceRoll (i, count) =
  ( r1 + r2 + r3 + 3, -- 3 for the mod 100 offset
    (r3, count + 3)
  )
  where
    r1 = (i + 1) `mod` 100
    r2 = (i + 2) `mod` 100
    r3 = (i + 3) `mod` 100

gameStepInt :: Game -> Int -> Game
gameStepInt (Game p1 p2 active dice) amount = Game newP1 newP2 newActive dice
  where
    newActive = (active + 1) `mod` 2
    newP1 = if active == 0 then moveAndScorePlayer p1 amount else p1
    newP2 = if active == 1 then moveAndScorePlayer p2 amount else p2

gameStep :: Game -> Game
gameStep (Game p1 p2 active dice) = gameStepInt (Game p1 p2 active newDice) amount
  where
    (amount, newDice) = getDeterminsticDiceRoll dice

newGame :: (Int, Int) -> Game
newGame (pos1, pos2) = Game (Player (pos1 - 1) 0) (Player (pos2 - 1) 0) 0 (-1, 0)

solution1 :: (Int, Int) -> Int
solution1 pos = loserScore * rollCount
  where
    game = newGame pos
    finalGame = until hasWinner gameStep game
    loserScore = case getWinner finalGame of
      Just (_, Player _ score) -> score
      _ -> error "Invalid winner"
    rollCount = getDiceRollCount finalGame

countUniverses :: Game -> (Int, Int)
countUniverses g
  | hasWinner g = case (g, getWinner g) of
    (Game p1 p2 _ _, Just (w, _)) -> if w == p1 then (1, 0) else (0, 1)
    _ -> error "Expected a winner"
-- There's got to be a better way of summing a list of tuples (maybe a fold?)
countUniverses g = sum *** sum $ unzip $ map mapFunc gameStates
  where
    gameStates =
      map
        (Data.Bifunctor.first (gameStepInt g))
        [(6, 7), (5, 6), (7, 6), (8, 3), (4, 3), (9, 1), (3, 1)] -- Move values and how many times they show up.
    mapFunc (g, count) = (p1Win * count, p2Win * count)
      where
        (p1Win, p2Win) = countUniverses g

solution2 :: (Int, Int) -> Int
solution2 pos = uncurry max $ countUniverses $ newGame pos

main = do
  print (solution1 (1, 2))
  print (solution2 (1, 2))
