import chess

# Endziel: Gesamtscore erstellen. Basiert auf Königsnähe und Randnähe (G = k + r).

# 1. Position der Könige herausfinden
# 2. Manhattan-Distanz berechnen (Nähe der Könige)
# 3. Randnähe des Königs berechnen (in die Ecke treiben)
# 4. Ergebnis zusammenfassen (G = k + r)

# Koordinaten des Feldes anhand der Königsposition herausfinden
def get_coordinates(piece_position):

    x = piece_position % 8
    y = piece_position // 8

    return x, y

# Positionen der Könige herausfinden
def extract_king_position(current_board):

    # Könige auf dem Brett finden
    white_king_on_board = current_board.pieces(chess.KING, chess.WHITE)
    black_king_on_board = current_board.pieces(chess.KING, chess.BLACK)

    # Nummer des Feldes herausfinden (0-63)
    white_king_square = list(white_king_on_board)[0]
    black_king_square = list(black_king_on_board)[0]

    print(f"White King Square:{white_king_square}")
    print(f"Black King Square:{black_king_square}")

    return white_king_square, black_king_square


def manhattan_distance(white_king_square, black_king_square):
    white_king_x, white_king_y = get_coordinates(white_king_square)
    black_king_x, black_king_y = get_coordinates(black_king_square)

    print(f"White King Position: {white_king_x}, {white_king_y}")
    print(f"Black King Position: {black_king_x}, {black_king_y}")

    # Manhattan-Distanz Score berechnen
    manhattan_distance_score = abs(white_king_x - black_king_x) + abs(white_king_y - black_king_y)

    print(f"Manhattan Distance Score: {manhattan_distance_score}")

    return manhattan_distance_score

# Kleinsten Abstand zum Rand finden
def edge_distance(black_king_position):
    # Koordinaten holen
    black_king_x, black_king_y = get_coordinates(black_king_position)

    # Abstand zu den Rändern berechnen
    distance_left = black_king_x
    distance_right = 7 - black_king_x
    distance_bottom = black_king_y
    distance_top = 7 - black_king_y

    print("Distances to Edges:")
    print(f"left: {distance_left}, right: {distance_right}, bottom: {distance_bottom}, top: {distance_top}")

    nearest_to_edge = min(distance_left, distance_right, distance_bottom, distance_top)

    print(f"Nearest to Edge: {nearest_to_edge}")

    return nearest_to_edge


def evaluate_board(current_board):
    print(str(current_board))
    print("Board Evaluation:")

    # Funktionen nutzen
    white_king_position, black_king_position = extract_king_position(current_board)
    manhattan_distance_score = manhattan_distance(white_king_position, black_king_position)
    edge_score = edge_distance(black_king_position)

    # TO-DO: Gesamtscore berechnen (G = manhattan + edge) -> > oder < ? Daten invertieren oder nicht?

    return manhattan_distance_score, edge_score
