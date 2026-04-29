import chess

# Gewichte:
black_is_mated = 1000000
stalemate = -500000
center_weight = 4
manhattan_weight = 2
rook_weight = 1
INF = 10000000


# Positionen der Figuren herausfinden
def extract_positions(current_board):
    # Figuren auf dem Brett finden
    white_king_on_board = current_board.pieces(chess.KING, chess.WHITE)
    black_king_on_board = current_board.pieces(chess.KING, chess.BLACK)
    # Nummer des Feldes herausfinden (0-63)
    white_king_square = list(white_king_on_board)[0]
    black_king_square = list(black_king_on_board)[0]
    return white_king_square, black_king_square

# Koordinaten des Feldes anhand der Königsposition herausfinden
def get_coordinates(piece_position):
    x = piece_position % 8
    y = piece_position // 8
    return x, y

def distance_to_center (black_king_square):
    black_king_x, black_king_y = get_coordinates(black_king_square)
    # Größter Wert (Abstand zur Mitte) ist 3, kleinster Wert ist 0
    distance_x = max(3-black_king_x, black_king_x-4)
    distance_y = max(3-black_king_y, black_king_y-4)
    return distance_x + distance_y

def manhattan_distance(white_king_square, black_king_square):
    white_king_x, white_king_y = get_coordinates(white_king_square)
    black_king_x, black_king_y = get_coordinates(black_king_square)
    manhattan_distance_score = abs(white_king_x - black_king_x) + abs(white_king_y - black_king_y)
    return 14 - manhattan_distance_score

def rook_positioning(current_board, black_king_square):
    rook = current_board.pieces(chess.ROOK, chess.WHITE)
    if len(rook) == 0:
        return 0
    rook_square = list(rook)[0]

    rook_x, rook_y = get_coordinates(rook_square)
    black_king_x, black_king_y = get_coordinates(black_king_square)
    vertical_distance = abs(black_king_y - rook_y)
    horizontal_distance = abs(black_king_x - rook_x)
    return abs(vertical_distance - horizontal_distance)

def minimax(current_board, depth, ply=0, alpha=-INF, beta=INF):
    white_to_move = (current_board.turn == chess.WHITE)
    if current_board.is_checkmate():
        return black_is_mated - ply, None
    if current_board.is_insufficient_material() or current_board.can_claim_draw() or current_board.is_stalemate():
        return stalemate, None
    if depth == 0:
        return evaluate_board(current_board), None
    legal_moves_list = list(current_board.legal_moves)
    if len(legal_moves_list) == 0:
        return stalemate, None

    if white_to_move:
        best_score = -INF
        best_move = None
        for move in legal_moves_list:
            current_board.push(move)
            score, _ = minimax(current_board, depth -1, ply + 1, alpha, beta)
            current_board.pop()
            if score > best_score:
                best_score = score
                best_move = move
            if best_score > alpha:
                alpha = best_score
            if best_score >= beta:
                break
        return best_score, best_move
    else:
        best_score = INF
        best_move = None
        for move in legal_moves_list:
            current_board.push(move)
            score, _ = minimax(current_board, depth -1, ply + 1, alpha, beta)
            current_board.pop()
            if score < best_score:
                best_score = score
                best_move = move
            if best_score < beta:
                beta = best_score
            if alpha >= beta:
                break
        return best_score, best_move

def evaluate_board(current_board):
    white_king_square, black_king_square = extract_positions(current_board)
    score = center_weight * distance_to_center(black_king_square)
    score += manhattan_weight * manhattan_distance(white_king_square, black_king_square)
    score += rook_weight * rook_positioning(current_board, black_king_square)
    return score

def play_game(current_board, depth):
    board = current_board
    move_count = 0
    print("Starting position:")
    print(board)

    while not board.is_checkmate():
        score, best_move = minimax(board, depth)
        if best_move is None and score == stalemate:
            print("Stalemate. Game over.")
            break
        board.push(best_move)
        move_count += 1
        print(f"Move {move_count}: {best_move}, Score: {score},")

    print("Position after the game ended:")
    print(board)
    return move_count