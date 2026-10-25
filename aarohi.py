"""Maze Solver mini project: BFS (shortest path) and DFS (path search)."""

from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path


SAMPLE_MAZE = [
    "###############",
    "#S..#......#..#",
    "#.#.#.####.#..#",
    "#.#......#....#",
    "#.######.###..#",
    "#......#......#",
    "###.##.#.######",
    "#...##.#......#",
    "#.####.######.#",
    "#............G#",
    "###############",
]

# Deterministic neighbor ordering: up, right, down, left.
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
Position = tuple[int, int]


def load_maze(lines: list[str]) -> tuple[list[list[str]], Position, Position]:
    """Validate and parse a rectangular maze containing one S and one G."""
    rows = [line.strip() for line in lines if line.strip()]
    if not rows:
        raise ValueError("Maze is empty.")
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise ValueError("Every maze row must have the same number of characters.")

    maze = [list(row) for row in rows]
    starts = [(r, c) for r, row in enumerate(maze) for c, cell in enumerate(row) if cell == "S"]
    goals = [(r, c) for r, row in enumerate(maze) for c, cell in enumerate(row) if cell == "G"]
    allowed = {"#", ".", "S", "G"}
    if any(cell not in allowed for row in maze for cell in row):
        raise ValueError("Use only # (wall), . (open), S (start), and G (goal).")
    if len(starts) != 1 or len(goals) != 1:
        raise ValueError("Maze must contain exactly one S and exactly one G.")
    return maze, starts[0], goals[0]


def solve(maze: list[list[str]], start: Position, goal: Position, algorithm: str):
    """Return (path, number_of_visited_cells); path is None when unreachable."""
    rows, cols = len(maze), len(maze[0])
    frontier = deque([start])
    visited = {start}
    parent: dict[Position, Position | None] = {start: None}

    while frontier:
        current = frontier.popleft() if algorithm == "bfs" else frontier.pop()
        if current == goal:
            break

        for dr, dc in DIRECTIONS:
            nxt = (current[0] + dr, current[1] + dc)
            r, c = nxt
            if (0 <= r < rows and 0 <= c < cols
                    and maze[r][c] != "#" and nxt not in visited):
                visited.add(nxt)
                parent[nxt] = current
                frontier.append(nxt)

    if goal not in parent:
        return None, len(visited)

    path = []
    current: Position | None = goal
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path, len(visited)


def render(maze: list[list[str]], path: list[Position] | None) -> str:
    display = [row.copy() for row in maze]
    if path:
        for r, c in path:
            if display[r][c] not in {"S", "G"}:
                display[r][c] = "*"
    return "\n".join("".join(row) for row in display)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve a grid maze using BFS and/or DFS.")
    parser.add_argument("--algorithm", choices=["bfs", "dfs", "both"], default="both",
                        help="BFS finds a shortest path; DFS finds a path (default: both).")
    parser.add_argument("--file", type=Path, help="Optional text file containing a maze.")
    args = parser.parse_args()

    try:
        lines = args.file.read_text(encoding="utf-8").splitlines() if args.file else SAMPLE_MAZE
        maze, start, goal = load_maze(lines)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    print("Maze legend: # wall, . open, S start, G goal, * path\n")
    algorithms = ["bfs", "dfs"] if args.algorithm == "both" else [args.algorithm]
    for algorithm in algorithms:
        path, visited_count = solve(maze, start, goal, algorithm)
        print(f"{algorithm.upper()} result:")
        if path is None:
            print("No path exists.")
        else:
            print(render(maze, path))
            print(f"Path length: {len(path) - 1} moves")
        print(f"Cells visited: {visited_count}\n")


if __name__ == "__main__":
    main()
