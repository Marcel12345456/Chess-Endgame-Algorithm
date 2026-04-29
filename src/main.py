from src.board import random_endgame
from src.tablebase_api import get_tablebase_data
from src.engine import play_game
import csv

results = []
depth = 6

for i in range(1):
    currentBoard = random_endgame()
    fen = currentBoard.fen()
    engine_result = get_tablebase_data(fen)
    heuristic_result = play_game(currentBoard, depth)

    results.append({
        "iteration": i + 1,
        "fen": fen,
        "engine": engine_result.json()["dtm"],
        "heuristic": heuristic_result,
        "depth": depth,
    })

with open('results.csv', 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=['iteration', 'fen', 'heuristic', 'engine', 'depth'])
    writer.writeheader()
    writer.writerows(results)

for r in results:
    print(f"Run {r['iteration']}: Engine={r['engine']}, Heuristic={r['heuristic']}")