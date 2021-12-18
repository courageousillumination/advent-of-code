import Data.Either (fromRight)
import Data.Maybe
import Debug.Trace
import System.IO
import Text.ParserCombinators.Parsec

data Tree = Branch Tree Tree | Leaf Int deriving (Show, Eq)

data Crumb = LeftCrumb Tree | RightCrumb Tree deriving (Show, Eq)

type Breadcrumbs = [Crumb]

type Zipper = (Tree, Breadcrumbs)

isLeaf :: Zipper -> Bool
isLeaf (Leaf _, _) = True
isLeaf _ = False

isRight :: Zipper -> Bool
isRight (_, RightCrumb _ : _) = True
isRight _ = False

isLeft :: Zipper -> Bool
isLeft (_, LeftCrumb _ : _) = True
isLeft _ = False

isAtTop :: Zipper -> Bool
isAtTop (_, []) = True
isAtTop _ = False

isBasicPair :: Zipper -> Bool
isBasicPair (Branch (Leaf _) (Leaf _), _) = True
isBasicPair _ = False

goLeft :: Zipper -> Zipper
goLeft (Branch l r, bs) = (l, LeftCrumb r : bs)
goLeft _ = error "Can not run on a Leaf"

goRight :: Zipper -> Zipper
goRight (Branch l r, bs) = (r, RightCrumb l : bs)
goRight _ = error "Can not go right on a leaf"

goUp :: Zipper -> Zipper
goUp (t, LeftCrumb r : bs) = (Branch t r, bs)
goUp (t, RightCrumb l : bs) = (Branch l t, bs)
goUp (_, []) = error "Can not go up any further"

toRoot :: Zipper -> Zipper
toRoot = until (null . snd) goUp

upUntil :: (Zipper -> Bool) -> Zipper -> Maybe Zipper
upUntil pred z
  | pred z = Just z
  | isAtTop z = Nothing
  | otherwise = upUntil pred (goUp z)

getLeftNeighbor :: Zipper -> Maybe Zipper
getLeftNeighbor z = do
  z' <- upUntil isRight z
  return $ until isLeaf goRight (goLeft $ goUp z')

getRightNeighbor :: Zipper -> Maybe Zipper
getRightNeighbor z = do
  z' <- upUntil isLeft z
  return $ until isLeaf goLeft (goRight $ goUp z')

addVal :: Zipper -> Int -> Zipper
addVal (Leaf x, bs) y = (Leaf (x + y), bs)
addVal _ _ = error "Can only add to leaf"

refocus :: Zipper -> Breadcrumbs -> Zipper
refocus z [] = z
refocus z ((LeftCrumb _) : bs) = refocus (goLeft z) bs
refocus z ((RightCrumb _) : bs) = refocus (goRight z) bs

find :: (Zipper -> Bool) -> Zipper -> Maybe Zipper
find pred z
  | pred z = Just z
  | isLeaf z = Nothing
  | isJust left = left
  | isJust right = right
  | otherwise = Nothing
  where
    left = find pred (goLeft z)
    right = find pred (goRight z)

getExploding :: Zipper -> Maybe Zipper
getExploding = find (\z'@(_, crumbs) -> length crumbs >= 4 && isBasicPair z')

applyExploding :: Zipper -> Zipper
applyExploding z@(Branch (Leaf l) (Leaf r), bs) = tree3
  where
    tree1 = (Leaf 0, bs) -- Tree after inserting 0
    left = getLeftNeighbor tree1
    tree2 = if isNothing left then tree1 else addVal (fromJust left) l -- Update the left value
    refocused = refocus (toRoot tree2) (reverse bs)
    right = getRightNeighbor refocused
    tree3 = if isNothing right then tree2 else addVal (fromJust right) r -- Update the right value
applyExploding z = error $ "Can not explode a leaf" ++ show z

getSplit :: Zipper -> Maybe Zipper
getSplit = find pred
  where
    pred (Leaf x, _) = x >= 10
    pred _ = False

applySplit :: Zipper -> Zipper
applySplit (Leaf x, crumbs) =
  ( Branch
      (Leaf $ floor $ toRational x / 2)
      (Leaf $ ceiling $ toRational x / 2),
    crumbs
  )
applySplit _ = error "Can only split a leaf"

zipToTree :: Zipper -> Tree
zipToTree = fst . toRoot

prettyPrintTree :: Tree -> String
prettyPrintTree (Leaf x) = show x
prettyPrintTree (Branch t1 t2) = '[' : prettyPrintTree t1 ++ "," ++ prettyPrintTree t2 ++ "]"

day18 :: CharParser () Tree
day18 =
  toBranch
    <$> between
      (char '[')
      (char ']')
      (sepBy day18 (char ','))
    <|> number

number :: CharParser () Tree
number = Leaf . read <$> many1 digit

toBranch :: [Tree] -> Tree
toBranch [t1, t2] = Branch t1 t2
toBranch _ = error "Incorrect number of branches"

toTree :: String -> Tree
toTree input = fromRight undefined $ parse day18 "(unknown)" input

reduceStep :: Tree -> Maybe Tree
reduceStep t
  | isJust zExplode = Just $ zipToTree $ applyExploding (fromJust zExplode)
  | isJust zSplit = Just $ zipToTree $ applySplit (fromJust zSplit)
  | otherwise = Nothing
  where
    zExplode = getExploding (t, [])
    zSplit = getSplit (t, [])

reduce :: Tree -> Tree
reduce t = maybe t reduce (reduceStep t)

add :: Tree -> Tree -> Tree
add t1 t2 = reduce (Branch t1 t2)

magnitude :: Tree -> Int
magnitude (Leaf x) = x
magnitude (Branch l r) = 3 * magnitude l + 2 * magnitude r

solution1 :: [Tree] -> Int
solution1 trees = magnitude $ foldl1 add trees

solution2 :: [Tree] -> Int
solution2 trees = maximum $ [magnitude (add x y) | x <- trees, y <- trees, x /= y]

main = do
  handle <- openFile "input.txt" ReadMode
  contents <- hGetContents handle
  let trees = map toTree $ lines contents
  print (solution1 trees)
  print (solution2 trees)
  hClose handle
