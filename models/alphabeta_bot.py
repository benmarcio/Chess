import math
from board import Board

PIECE_VALUES = {
    1: 100,   # pawn
    2: 320,   # knight
    3: 330,   # bishop
    4: 500,   # rook
    5: 900,   # queen
    6: 20000, # king
}

def _clone_board(board: Board) -> Board:
    b = Board()
    b.squares = board.squares.copy()
    b.white_king_moved = board.white_king_moved
    b.black_king_moved = board.black_king_moved
    b.white_rook_kingside_moved = board.white_rook_kingside_moved
    b.white_rook_queenside_moved = board.white_rook_queenside_moved
    b.black_rook_kingside_moved = board.black_rook_kingside_moved
    b.black_rook_queenside_moved = board.black_rook_queenside_moved
    b.side_to_move = board.side_to_move
    b.en_passant_target = board.en_passant_target
    return b

def _generate_legal_moves(board: Board, color: int):
    saved_side = board.side_to_move
    board.side_to_move = color
    moves = []
    for r in range(8):
        for c in range(8):
            if int(board.squares[r][c]) * color > 0:
                for mv in board.get_valid_moves(r, c):
                    moves.append(((r, c), mv))
    board.side_to_move = saved_side
    return moves

def _evaluate(board: Board, bot_color: int) -> int:
    # Terminal: checkmate or stalemate
    if not board.has_any_legal_moves(board.side_to_move):
        if board.is_in_check(board.side_to_move):
            # side_to_move is checkmated
            return -PIECE_VALUES[6] if board.side_to_move == bot_color else PIECE_VALUES[6]
        return 0

    material = 0
    for r in range(8):
        for c in range(8):
            val = int(board.squares[r][c])
            if val != 0:
                material += PIECE_VALUES[abs(val)] * (1 if val > 0 else -1)

    # score from bot perspective
    return material if bot_color == 1 else -material

def _alpha_beta(board: Board, depth: int, alpha: float, beta: float, bot_color: int):
    if depth == 0:
        return _evaluate(board, bot_color), None

    legal_moves = _generate_legal_moves(board, board.side_to_move)
    if not legal_moves:
        return _evaluate(board, bot_color), None

    maximizing = (board.side_to_move == bot_color)

    best_move = None
    if maximizing:
        best_score = -math.inf
        for move in legal_moves:
            child = _clone_board(board)
            child.move_piece(move[0], move[1])
            score, _ = _alpha_beta(child, depth - 1, alpha, beta, bot_color)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score, best_move
    else:
        best_score = math.inf
        for move in legal_moves:
            child = _clone_board(board)
            child.move_piece(move[0], move[1])
            score, _ = _alpha_beta(child, depth - 1, alpha, beta, bot_color)
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score, best_move

def choose_move(board: Board, bot_color: int, depth: int = 3):
    _, move = _alpha_beta(board, depth, -math.inf, math.inf, bot_color)
    return move