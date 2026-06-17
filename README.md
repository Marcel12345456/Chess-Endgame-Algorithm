# Chess-Endgame-Algorithm

A university project that compares a hand-written minimax engine against the
[Lichess tablebase](https://tablebase.lichess.org/) on randomly generated
**KRK endgames** (white king + rook vs. black king). It forms the foundation of a
scientific paper in which the distance to mate of both methods is compared.

For each random position the project records two numbers (both in **half-moves / plies**):

- **tablebase (DTM):** the perfect-play distance to mate from the Lichess tablebase.
- **heuristic:** how many half-moves the custom engine actually needed to reach mate
  using minimax + alpha–beta with a simple evaluation function.

The results are written to `src/results/results_depth{depth}.csv`.

## Project layout

```
schach_decision_tree/
├── src/
│   ├── __init__.py
│   ├── board.py           # Generates random valid KRK positions
│   ├── engine.py          # Minimax + alpha–beta and heuristic evaluation
│   ├── tablebase_api.py   # Wrapper around the Lichess tablebase HTTP API
│   ├── main.py            # Entry point: runs the comparison, writes the CSV
│   ├── visualize.py       # Reads the CSVs and generates the analysis plots
│   └── results/           # Generated CSVs and PNGs (gitignored)
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
   - rook alignment on the same rank/file as the black king.

   Weights are defined at the top of `src/engine.py`.

## Setup

Requires Python 3.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run the experiment

```bash
python -m src.main
```

This plays out the random positions and writes
`src/results/results_depth{depth}.csv` with the columns:

| iteration | fen | heuristic | tablebase | depth |
|-----------|-----|-----------|-----------|-------|

- `heuristic` — half-moves the custom engine needed.
- `tablebase` — optimal half-moves to mate (DTM) from the Lichess tablebase.

## Generate the plots

```bash
python -m src.visualize
```

Without arguments it reads every `src/results/results_depth*.csv`; you can also pass
files explicitly (`python -m src.visualize src/results/results_depth4.csv ...`).
Per search depth it writes three PNGs into `src/results/`:

- `diff_histogramm_depth{d}.png` — distribution of (played − optimal) half-moves.
- `ratio_kategorien_depth{d}.png` — efficiency relative to the optimum, bucketed.
- `scatter_alpha_depth{d}.png` — played vs. optimal per position (density via opacity).

It also prints the median and mean of the difference and the ratio per depth.

## Configuration

The two main knobs sit at the top of `src/main.py`:

- `depth` — search depth for the minimax engine (default `4`).
- the `for i in range(...)` loop — number of random positions to evaluate
  (default `200`).

Increase the depth for more reliable, more efficient mates, but note that deeper
searches scale roughly exponentially. Depth 6 is a good balance of reliable
checkmate and moderate running time; depth 4 serves as a lower-depth comparison.

## Dependencies

- [`python-chess`](https://pypi.org/project/chess/) — board representation,
  move generation and rules.
- [`requests`](https://pypi.org/project/requests/) — HTTP calls to the
  Lichess tablebase.
- [`pandas`](https://pypi.org/project/pandas/),
  [`numpy`](https://pypi.org/project/numpy/),
  [`matplotlib`](https://pypi.org/project/matplotlib/) — data analysis and plots
  in `visualize.py`.
