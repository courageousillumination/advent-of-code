defmodule BingoBoard do
  use Agent

  def start_link(board) do
    Agent.start_link(fn -> {board, -1} end)
  end

  def get_board(pid) do
    Agent.get(pid, fn {board, _} -> board end)
  end

  def get_score(pid) do
    Agent.get(pid, fn {_, score} -> score end)
  end

  def has_won(pid) do
    board = get_board(pid)
    is_winner(board)
  end

  def score(pid, num) do
    board_score = get_board(pid) |> Enum.filter(fn x -> x != -1 end) |> Enum.sum()
    final_score = board_score * num
    Agent.update(pid, fn {board, _} -> {board, final_score} end)
    final_score
  end

  def is_winner(board) do
    won_row =
      Enum.chunk_every(board, 5)
      |> Enum.map(&Enum.sum/1)
      |> Enum.member?(-5)

    won_column =
      0..5
      |> Enum.map(&Enum.drop(board, &1))
      |> Enum.map(&Enum.take_every(&1, 5))
      |> Enum.map(&Enum.sum/1)
      |> Enum.member?(-5)

    won_column or won_row
  end

  def play_move(pid, move) do
    Agent.update(pid, fn {board, score} ->
      {Enum.map(board, fn x ->
         if x == move do
           -1
         else
           x
         end
       end), score}
    end)
  end
end

defmodule Main do
  def solution(input) do
    [moves | boards] = String.split(input, "\n\n")
    moves = String.split(moves, ",") |> Enum.map(&String.to_integer/1)

    boards =
      boards
      |> Enum.map(&String.split/1)
      |> Enum.map(&Enum.map(&1, fn x -> String.to_integer(x) end))
      |> Enum.map(&BingoBoard.start_link/1)
      |> Enum.unzip()
      |> elem(1)

    Enum.each(moves, fn move ->
      Enum.each(boards, fn board ->
        BingoBoard.play_move(board, move)

        if BingoBoard.has_won(board) and BingoBoard.get_score(board) == -1 do
          IO.inspect(BingoBoard.score(board, move))
        end
      end)
    end)
  end

  def main do
    {:ok, content} = File.read("input.txt")
    IO.inspect(solution(content))
  end
end

Main.main()
