# Chess-Engame-Algorithm

A university project that compares a hand-written minimax engine against the
[Lichess Syzygy tablebase](https://tablebase.lichess.org/) on randomly generated
**KRK endgames** (White king + rook vs. black king). It forms the foundation of a scientific paper, in which I compare the distance to mate of both methods with each other.

For each random position the project records two numbers:

- **Engine (DTM):** the perfect-play distance to mate from the tablebase.
- **Heuristic:** how many moves the custom engine actually needed to reach mate
  using minimax + alpha–beta with a simple evaluation function.

The results are written to `results.csv`.

## Project layout

```
schach_decision_tree/
├── src/
│   ├── __init__.py
│   ├── board.py           # Generates random valid KRK positions
│   ├── engine.py          # Minimax + alpha–beta and heuristic evaluation
│   ├── tablebase_api.py   # Wrapper around the Lichess tablebase HTTP API
│   └── main.py            # Entry point: runs the comparison, writes CSV
└── requirements.txt
```

## How it works

1. `board.random_endgame()` places a black king, white king and white rook on
   random squares until the resulting position is legal.
2. `tablebase_api.get_tablebase_data(fen)` queries the Lichess tablebase and
   returns the optimal distance-to-mate.
3. `engine.play_game(board, depth)` plays the position out using
   `engine.minimax(...)` with alpha–beta pruning. The score combines:
   - distance of the black king to the center (drive it to the edge),
   - inverted Manhattan distance between the two kings (push them together),
   - rook alignment relative to the black king.

   Weights are defined at the top of `src/engine.py`.

## Setup

Requires Python 3.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python -m src.main
```

This prints the starting position, every move played, and finally writes
`results.csv` with the columns:

| iteration | fen | heuristic | engine | depth |
|-----------|-----|-----------|--------|-------|

## Configuration

The two main knobs sit at the top of `src/main.py`:

- `depth` — search depth for the minimax engine (default `6`).
- The `for i in range(...)` loop — number of random positions to evaluate
  (default `1`).

Increase both to gather more data - deeper searches scale roughly exponentially.
I recommend using depth 6 for reliable checkmate.

## Dependencies

- [`python-chess`](https://pypi.org/project/chess/) — board representation,
  move generation and rules.
- [`requests`](https://pypi.org/project/requests/) — HTTP calls to the
  Lichess tablebase.
