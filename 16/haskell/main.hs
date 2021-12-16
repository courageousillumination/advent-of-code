import Data.Char (digitToInt)
import Data.List
import Debug.Trace
import Numeric (readHex)
import System.IO
import Text.Printf

type Bit = Int

data Packet
  = LiteralPacket Int Int
  | OperatorPacket Int Int [Packet]
  deriving (Show)

-- Generic bit twiddling stuff...
toDec :: String -> Int
toDec = foldl' (\acc x -> acc * 2 + digitToInt x) 0

bitsToInt :: [Bit] -> Int
bitsToInt bits = toDec $ concatMap show bits

charToBits :: Char -> [Bit]
charToBits c = case readHex [c] of
  (x, _) : _ -> map digitToInt $ printf "%04b" (x :: Int)
  _ -> error "Failed to parse character"

toBitArray :: String -> [Bit]
toBitArray = concatMap charToBits

getLiteralBits :: [Bit] -> ([Bit], [Bit])
getLiteralBits (0 : xs) = splitAt 4 xs
getLiteralBits (1 : xs) = (take 4 xs ++ content, rest)
  where
    (content, rest) = getLiteralBits (drop 4 xs)
getLiteralBits _ = error "Unexpected literal bits"

getLiteralValue :: [Bit] -> (Int, [Bit])
getLiteralValue bits = (bitsToInt val, rest)
  where
    (val, rest) = getLiteralBits bits

getSubPacketLengthHelper :: Int -> ([Packet], [Bit]) -> ([Packet], [Bit])
getSubPacketLengthHelper remaining (packets, bits) =
  if remaining == 0
    then (packets, bits)
    else getSubPacketLengthHelper (remaining - (length bits - length rest)) (packets ++ [parsed], rest)
  where
    (parsed, rest) = parsePacket bits

getSubPackets :: [Bit] -> ([Packet], [Bit])
getSubPackets (0 : bits) = getSubPacketLengthHelper subLength ([], drop 15 bits)
  where
    subLength = bitsToInt $ take 15 bits
getSubPackets (1 : bits) = foldl' helper ([], drop 11 bits) [1 .. subPacketCount]
  where
    subPacketCount = bitsToInt $ take 11 bits
    helper (packets, remainingBits) _ = (packets ++ [parsed], rest)
      where
        (parsed, rest) = parsePacket remainingBits
getSubPackets _ = error "Unexpected bits when parsing sub packets"

buildLiteralPacket :: Int -> [Bit] -> (Packet, [Bit])
buildLiteralPacket version bits = (LiteralPacket version val, rest)
  where
    (val, rest) = getLiteralValue bits

buildOperatorPacket :: Int -> Int -> [Bit] -> (Packet, [Bit])
buildOperatorPacket version opCode bits = (OperatorPacket version opCode packets, rest)
  where
    (packets, rest) = getSubPackets bits

parsePacket :: [Bit] -> (Packet, [Bit])
parsePacket bits = case packetType of
  4 -> buildLiteralPacket version $ drop 6 bits
  _ -> buildOperatorPacket version packetType $ drop 6 bits
  where
    version = bitsToInt $ take 3 bits
    packetType = bitsToInt $ take 3 $ drop 3 bits

sumVersions :: Packet -> Int
sumVersions (LiteralPacket version _) = version
sumVersions (OperatorPacket version _ packets) = version + sum (map sumVersions packets)

evaluate :: Packet -> Int
evaluate (LiteralPacket _ val) = val
evaluate (OperatorPacket _ 0 packets) = sum $ map evaluate packets
evaluate (OperatorPacket _ 1 packets) = product $ map evaluate packets
evaluate (OperatorPacket _ 2 packets) = minimum $ map evaluate packets
evaluate (OperatorPacket _ 3 packets) = maximum $ map evaluate packets
evaluate (OperatorPacket _ 5 packets) = if evaluate (head packets) > evaluate (last packets) then 1 else 0
evaluate (OperatorPacket _ 6 packets) = if evaluate (head packets) < evaluate (last packets) then 1 else 0
evaluate (OperatorPacket _ 7 packets) = if evaluate (head packets) == evaluate (last packets) then 1 else 0
evaluate _ = error "Unknown operator"

solution1 :: String -> Int
solution1 = sumVersions . fst . parsePacket . toBitArray

solution2 :: String -> Int
solution2 = evaluate . fst . parsePacket . toBitArray

main = do
  handle <- openFile "input.txt" ReadMode
  contents <- hGetContents handle
  print (solution1 contents)
  print (solution2 contents)
  hClose handle
