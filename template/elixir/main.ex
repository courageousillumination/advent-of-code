defmodule Main do

  def solution input do
    result = String.split(input, "\n")
    List.first(result)
  end

  def main do
    {:ok, content} = File.read("input.txt")
    IO.puts solution(content)
  end

end

Main.main
