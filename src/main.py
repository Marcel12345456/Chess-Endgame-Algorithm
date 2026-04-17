from src.board import random_endgame
from src.tablebase_api import get_tablebase_data
from src.engine import evaluate_board

currentBoard = random_endgame()
fen = currentBoard.fen()


engine_result = get_tablebase_data(fen)

heuristic_result = evaluate_board(currentBoard)


print("FEN: ", fen)
print("Mate based on heuristics: ", heuristic_result)
print("Mate based on engine: ", engine_result.json()["dtm"])