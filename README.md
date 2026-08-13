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

## Known limitation: black does not play perfect defense

**The two numbers are not yet a clean comparison, and the difference between them
should not be read as "how far the engine is from optimal play."**

`tablebase` is the distance to mate assuming *both* sides play perfectly — white
mates as fast as possible, black survives as long as possible. `heuristic` is the
number of half-moves actually played in a game where **both** sides are driven by
the same minimax search over the same evaluation function
(`engine.evaluate_board`). That function only scores white's mating progress:
black king pushed to the edge, kings close together, rook aligned. Black moves by
minimizing that white-centric score at the same fixed depth — it has no objective
of its own and no notion of prolonging its survival.

So `heuristic − tablebase` conflates two separate error sources:

1. white's imperfect mating technique (the thing the project intends to measure), and
2. black's imperfect defense (an artifact of the setup).

Because a defender that minimizes white's heuristic is not the same as a defender
that maximizes distance to mate, black's play can both shorten and lengthen the
game relative to optimal defense, and the two effects cannot be separated in the
current CSVs. Treat the recorded difference as an upper-bound-ish indication of
engine quality, not as a measurement of it.

Making this a valid comparison requires replacing black's move selection with
tablebase-optimal defense (query the tablebase for black's move each ply) and
re-running the experiment. That is not implemented.

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

- `depth` — search depth for the minimax engine (default `6`).
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
