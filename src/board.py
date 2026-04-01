import chess
import random

def random_engame():

    while True:
        board = chess.Board()

        board.clear()

        field = random.sample(range(64), 3)

        black_king = field[0]
        white_king = field[1]
        white_rook = field[2]

        board.set_piece_at(black_king, chess.Piece(chess.KING, chess.BLACK))
        board.set_piece_at(white_king, chess.Piece(chess.KING, chess.WHITE))
        board.set_piece_at(white_rook, chess.Piece(chess.ROOK, chess.WHITE))

        board.turn = chess.WHITE

        if board.is_valid():
            return board

if __name__ == "__main__":
    test_board = random_engame()
    print("Random Endgame: \n", test_board, "\n")
    print("FEN-String: \n ", test_board.fen())