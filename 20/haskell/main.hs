import Data.List
import Debug.Trace
import System.IO

type Position = (Int, Int)

type RefinementAlgorithm = [Int]

data ImageState
  = Image
      [[Int]] -- Pixels
      Int -- Void state
  deriving (Show)

-- Convert a list of bits to a decimal number.
toDec :: [Int] -> Int
toDec = foldl' (\acc x -> acc * 2 + x) 0

-- Get all neighbors (in correct order)
getNeighbors :: Position -> [Position]
getNeighbors (x, y) = [(x + dx, y + dy) | dy <- [-1, 0, 1], dx <- [-1, 0, 1]]

-- Refine a single pixel
refinePixel :: ImageState -> RefinementAlgorithm -> Position -> Int
refinePixel i alg pos = alg !! index
  where
    indexBits = map (getPixel i) (getNeighbors pos)
    index = toDec indexBits

-- Get pixels, with special accomodation for void pixels.
getPixel :: ImageState -> Position -> Int
getPixel (Image pixels void) (x, y) =
  if y < 0 || y >= length pixels || x < 0 || x >= length pixels
    then void
    else pixels !! y !! x

-- Expands an image by 1 px in all directions
expandImage :: ImageState -> ImageState
expandImage (Image pix void) = Image newPix void
  where
    emptyRow = replicate (length pix + 2) void
    newPix = (emptyRow : map (\x -> void : x ++ [void]) pix) ++ [emptyRow]

-- Get a map of indicies for updating.
indicies :: ImageState -> [[Position]]
indicies (Image pix _) =
  [[(x, y) | x <- [0 .. length pix -1]] | y <- [0 .. length pix -1]]

runRefinement :: RefinementAlgorithm -> ImageState -> ImageState
runRefinement refine i@(Image pix void) = Image newPixels newVoid
  where
    expanded = expandImage i
    newPixels = map (map $ refinePixel expanded refine) (indicies expanded)
    newVoid = if void == 0 && head refine == 1 then 1 else 0

lightToInt :: Char -> Int
lightToInt '.' = 0
lightToInt '#' = 1
lightToInt _ = error "Invalid light value"

intToLight :: Int -> Char
intToLight 0 = '.'
intToLight 1 = '#'
intToLight _ = error "Invalid light value"

parseRefinementAlgorithm :: String -> RefinementAlgorithm
parseRefinementAlgorithm = map lightToInt

parseImage :: [String] -> ImageState
parseImage x = Image (map (map lightToInt) x) 0

countPixels :: ImageState -> Int
countPixels (Image pix _) = sum $ map sum pix

solution :: String -> Int -> Int
solution contents steps = countPixels finalImage
  where
    l = lines contents
    alg = parseRefinementAlgorithm $ head l
    image = parseImage $ drop 2 l
    finalImage = iterate (runRefinement alg) image !! steps

prettyPrintImage :: ImageState -> String
prettyPrintImage (Image pix _) = intercalate "\n" $ map (map intToLight) pix

main = do
  handle <- openFile "input.txt" ReadMode
  contents <- hGetContents handle
  print (solution contents 2)
  print (solution contents 50)
  hClose handle
