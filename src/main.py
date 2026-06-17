from src.board import random_endgame
from src.tablebase_api import get_tablebase_data
from src.engine import play_game
import csv
import os

depth = 4

results_dir = "src/results"
os.makedirs(results_dir, exist_ok=True)

with open(f"{results_dir}/results_depth{depth}.csv", 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=['iteration', 'fen', 'heuristic', 'tablebase', 'depth'])
    writer.writeheader()
    csv_file.flush()

    for i in range(200):
        currentBoard = random_endgame()
        fen = currentBoard.fen()
        engine_result = get_tablebase_data(fen)
        heuristic_result = play_game(currentBoard, depth)

        row = {
            "iteration": i + 1,
            "fen": fen,
            "tablebase": engine_result.json()["dtm"],
            "heuristic": heuristic_result,
            "depth": depth,
        }
        writer.writerow(row)
        csv_file.flush()
        print(f"Run {i + 1}/200 fertig: Engine={heuristic_result} plies, DTM={row['tablebase']}")