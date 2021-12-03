defmodule SubServer do
  use Agent

  def start_link() do
    Agent.start_link(fn -> {0, 0} end, name: __MODULE__)
  end

  def stop() do
    Agent.stop(__MODULE__, :normal)
  end

  def get_state() do
    Agent.get(__MODULE__, & &1)
  end

  def process_command(command) do
    Agent.update(__MODULE__, fn {x, y} ->
      case command do
        {:forward, d} -> {x + d, y}
        {:up, d} -> {x, y - d}
        {:down, d} -> {x, y + d}
      end
    end)
  end
end

defmodule Main do
  def solution(input) do
    SubServer.start_link()

    input
    |> String.split("\n")
    |> Enum.map(&String.split/1)
    |> Enum.map(fn [c, d] -> {String.to_atom(c), String.to_integer(d)} end)
    |> Enum.each(&SubServer.process_command/1)

    {x, y} = SubServer.get_state()
    x * y
  end

  def main do
    {:ok, content} = File.read("input.txt")
    IO.inspect(solution(content))
  end
end

Main.main()
