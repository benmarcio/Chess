KNIGHT_MOVES = [
    (1, 2), (1, -2), (-1, 2), (-1, -2),
    (2, 1), (2, -1), (-2, 1), (-2, -1)
]
ROOK_MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]
BISHOP_MOVES = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
KING_MOVES = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]
BISHOP_MOVES = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

class Piece:
    
    @staticmethod
    def get_knight_moves(board, row, col, piece_value):
        moves = []
               
        for move in KNIGHT_MOVES:
            row_change, col_change = move
            new_row = row + row_change
            new_col = col + col_change
            
            if board.is_on_board(new_row, new_col):
                
                target_square = board.squares[new_row][new_col]
                
                
                if target_square * piece_value > 0:
                    continue # Blocked by friend
                # If we get here, it's empty or enemy -> Valid!
                moves.append((new_row, new_col))
                
        return moves

    @staticmethod
    def get_rook_moves(board, row, col, piece_value):
        moves = []

        for move in ROOK_MOVES:
            row_dir, col_dir = move
            new_row = row + row_dir
            new_col = col + col_dir

            while board.is_on_board(new_row, new_col):
                target = board.squares[new_row][new_col]

                if target == 0:
                    moves.append((new_row, new_col))
                    new_row += row_dir
                    new_col += col_dir
                    continue

                
                if target * piece_value > 0:
                    break

                moves.append((new_row, new_col))
                break
        return moves

    @staticmethod
    def get_bishop_moves(board, row, col, piece_value):
        moves = []

        for move in BISHOP_MOVES:
            row_dir, col_dir = move
            new_row = row + row_dir
            new_col = col + col_dir

            while board.is_on_board(new_row, new_col):
                target = board.squares[new_row][new_col]

                if target == 0:
                    moves.append((new_row, new_col))
                    new_row += row_dir
                    new_col += col_dir
                    continue

                if target * piece_value > 0:
                    break

                moves.append((new_row, new_col))
                break

        return moves

    @staticmethod
    def get_queen_moves(board, row, col, piece_value):
        # rook + bishop
        moves = []
        moves.extend(Piece.get_rook_moves(board, row, col, piece_value))
        moves.extend(Piece.get_bishop_moves(board, row, col, piece_value))
        return moves

    @staticmethod
    def get_king_moves(board, row, col, piece_value):
        moves = []

        for d in KING_MOVES:
            new_row = row + d[0]
            new_col = col + d[1]
            if not board.is_on_board(new_row, new_col):
                continue
            target = board.squares[new_row][new_col]
            if target * piece_value > 0:
                continue
            moves.append((new_row, new_col))

        return moves

    @staticmethod
    def get_pawn_moves(board, row, col, piece_value):
        moves = []

        # direction: white (positive) moves up (row-1), black moves down (row+1)
        direction = -1 if piece_value > 0 else 1

        
        fr = row + direction
        if board.is_on_board(fr, col) and int(board.squares[fr][col]) == 0:
            moves.append((fr, col))

            # Two squares from starting rank
            start_row = 6 if piece_value > 0 else 1
            fr2 = row + 2 * direction
            if row == start_row and board.is_on_board(fr2, col) and int(board.squares[fr2][col]) == 0:
                moves.append((fr2, col))

        # Captures
        for dc in (-1, 1):
            cr = row + direction
            cc = col + dc
            if board.is_on_board(cr, cc):
                target = int(board.squares[cr][cc])
                if target * piece_value < 0:
                    moves.append((cr, cc))
                # En-passant: target square may be empty but equal to board.en_passant_target
                elif hasattr(board, 'en_passant_target') and board.en_passant_target == (cr, cc):
                    moves.append((cr, cc))

        return moves
