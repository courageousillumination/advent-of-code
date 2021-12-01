import System.IO

asInt :: String -> Int
asInt = read

solution :: String -> Int
solution input =
  let vals = map asInt $ lines input
   in head vals

main = do
  handle <- openFile "input.txt" ReadMode
  contents <- hGetContents handle
  print (solution contents)
  hClose handle
