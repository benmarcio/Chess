import numpy as np
from piece import Piece


class Board:
    def __init__(self):
        
        self.squares = np.zeros((8, 8))

        #black start
        self.squares[0] = [-4, -2, -3, -5, -6, -3, -2, -4] #back line
        self.squares[1] = [-1] * 8 # pawns

        #white start
        self.squares[6] = [1] * 8
        self.squares[7] = [4, 2, 3, 5, 6, 3, 2, 4]

        # flags for rochade
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_rook_kingside_moved = False
        self.white_rook_queenside_moved = False
        self.black_rook_kingside_moved = False
        self.black_rook_queenside_moved = False
        
        self.side_to_move = 1
        
        self.en_passant_target = None
        
        # Track move history for detecting repetition and fifty-move rule
        self.move_history = []  # List of board positions (as tuples for hashing)
        self.moves_since_capture_or_pawn = 0  # For fifty-move rule


    def add_piece(self, piece, row, col):
        
        self.squares[row][col] = piece

    def move_piece(self, start_pos, end_pos):
        initial_row, initial_col = start_pos
        final_row, final_col = end_pos
        piece = self.squares[initial_row][initial_col]
        
        # Save what's at the destination BEFORE any moves (for capture detection)
        captured_piece = self.squares[final_row][final_col]
        is_pawn_move = abs(int(piece)) == 1
        
        # 1. HANDLE EN PASSANT CAPTURE
        # If a pawn moves diagonally to an empty square, it MUST be En Passant
        if abs(piece) == 1 and self.squares[final_row][final_col] == 0 and initial_col != final_col:
            # The captured pawn is on the same row as the start, at the final column
            self.squares[initial_row][final_col] = 0 

        # 2. UPDATE EN PASSANT TARGET
        # If a pawn moves 2 squares, set the target square behind it
        if abs(piece) == 1 and abs(final_row - initial_row) == 2:
            mid_row = (initial_row + final_row) // 2
            self.en_passant_target = (mid_row, initial_col)
        else:
            self.en_passant_target = None

        prev_en_passant = self.en_passant_target

        if int(piece) == 6:
            self.white_king_moved = True
        if int(piece) == -6:
            self.black_king_moved = True
        # Rooks
        if int(piece) == 4:
            if (initial_row, initial_col) == (7, 7):
                self.white_rook_kingside_moved = True
            if (initial_row, initial_col) == (7, 0):
                self.white_rook_queenside_moved = True
        if int(piece) == -4:
            if (initial_row, initial_col) == (0, 7):
                self.black_rook_kingside_moved = True
            if (initial_row, initial_col) == (0, 0):
                self.black_rook_queenside_moved = True

        if abs(int(piece)) == 6 and initial_row == final_row and abs(final_col - initial_col) == 2:
            # Determine rook source/target
            if final_col == 6:  # kingside
                rook_src_col = 7
                rook_dst_col = 5
            elif final_col == 2:  # queenside
                rook_src_col = 0
                rook_dst_col = 3
            else:
                rook_src_col = None

            self.squares[final_row][final_col] = piece
            self.squares[initial_row][initial_col] = 0

            # Move rook if present
            if rook_src_col is not None and self.is_on_board(initial_row, rook_src_col):
                self.squares[initial_row][rook_dst_col] = self.squares[initial_row][rook_src_col]
                # mark rook moved flag based on color and side
                rook_val = int(self.squares[initial_row][rook_dst_col])
                if rook_val == 4:
                    # white rook moved
                    if rook_src_col == 7:
                        self.white_rook_kingside_moved = True
                    if rook_src_col == 0:
                        self.white_rook_queenside_moved = True
                if rook_val == -4:
                    if rook_src_col == 7:
                        self.black_rook_kingside_moved = True
                    if rook_src_col == 0:
                        self.black_rook_queenside_moved = True

                self.squares[initial_row][rook_src_col] = 0
            # flip side to move after successful castling
            self.side_to_move *= -1
            return

        
        # Handle en-passant capture: if moving pawn to previous en_passant_target, remove the captured pawn
        if abs(int(piece)) == 1 and prev_en_passant is not None and (final_row, final_col) == tuple(prev_en_passant):
            # remove the pawn that moved two squares last turn
            direction = -1 if int(piece) > 0 else 1
            captured_row = final_row - direction
            self.squares[captured_row][final_col] = 0

        self.squares[final_row][final_col] = piece
        self.squares[initial_row][initial_col] = 0

        # Pawn double move -> set en_passant target for opponent, otherwise clear
        if abs(int(piece)) == 1 and abs(final_row - initial_row) == 2:
            ep_row = (initial_row + final_row) // 2
            self.en_passant_target = (ep_row, final_col)
        else:
            self.en_passant_target = None

        # Promotion: promote pawn to queen (5) when reaching last rank
        if int(piece) == 1 and final_row == 0:
            self.squares[final_row][final_col] = 5
        if int(piece) == -1 and final_row == 7:
            self.squares[final_row][final_col] = -5
        
        # Update fifty-move rule counter
        if captured_piece != 0 or is_pawn_move:
            self.moves_since_capture_or_pawn = 0
        else:
            self.moves_since_capture_or_pawn += 1
        
        # flip side to move after normal move
        self.side_to_move *= -1
        
        # Store current position in move history AFTER flipping side_to_move
        board_state = self._get_board_state()
        self.move_history.append(board_state)

    def _get_board_state(self):
        """Get a hashable representation of the board state including side to move, castling, and en passant."""
        # Convert numpy array to nested tuple properly
        board_tuple = tuple(tuple(int(x) for x in row) for row in self.squares)
        
        # Include castling rights and en passant in the state
        castling = (
            self.white_king_moved,
            self.black_king_moved,
            self.white_rook_kingside_moved,
            self.white_rook_queenside_moved,
            self.black_rook_kingside_moved,
            self.black_rook_queenside_moved
        )
        
        # Convert en passant to tuple or None
        ep = tuple(self.en_passant_target) if self.en_passant_target else None
        
        return (board_tuple, self.side_to_move, castling, ep)
    
    def is_threefold_repetition(self):
        """Check if the current position has been repeated three times."""
        # Need at least 9 half-moves for a real threefold repetition
        # (positions can only repeat after both players have moved at least twice)
        if len(self.move_history) < 9:
            return False
        
        # Get current state (already stored with correct side_to_move)
        current_state = self._get_board_state()
        
        # Count occurrences in the entire history
        count = 0
        for state in self.move_history:
            if state == current_state:
                count += 1
                if count >= 3:
                    return True
        
        return False
    
    def is_fifty_move_rule(self):
        """Check if fifty moves have passed without capture or pawn move."""
        return self.moves_since_capture_or_pawn >= 100  # 100 half-moves = 50 full moves

    def is_on_board(self, row, col):
        return 0 <= row <= 7 and 0 <= col <= 7

    def is_square_attacked(self, row, col, by_color):
        # Pawns
        pawn_row = row + by_color
        for dc in (-1, 1):
            pr = pawn_row
            pc = col + dc
            if self.is_on_board(pr, pc):
                if int(self.squares[pr][pc]) == 1 * by_color:
                    return True

        # Knights
        from piece import KNIGHT_MOVES
        for dr, dc in KNIGHT_MOVES:
            r = row + dr
            c = col + dc
            if self.is_on_board(r, c):
                if int(self.squares[r][c]) == 2 * by_color:
                    return True

        # Rooks & Queens (straight lines)
        straight_dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in straight_dirs:
            r = row + dr
            c = col + dc
            while self.is_on_board(r, c):
                val = int(self.squares[r][c])
                if val != 0:
                    if val * by_color > 0 and (abs(val) == 4 or abs(val) == 5):
                        return True
                    break
                r += dr
                c += dc

        # Bishops & Queens (diagonals)
        diag_dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in diag_dirs:
            r = row + dr
            c = col + dc
            while self.is_on_board(r, c):
                val = int(self.squares[r][c])
                if val != 0:
                    if val * by_color > 0 and (abs(val) == 3 or abs(val) == 5):
                        return True
                    break
                r += dr
                c += dc

        # King (adjacent)
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r = row + dr
                c = col + dc
                if self.is_on_board(r, c):
                    if int(self.squares[r][c]) == 6 * by_color:
                        return True

        return False

    def is_in_check(self, color):
        # Find king
        king_val = 6 * color
        for r in range(8):
            for c in range(8):
                if int(self.squares[r][c]) == king_val:
                    return self.is_square_attacked(r, c, -color)
        return False
    
    def get_valid_moves(self, row, col):
        piece_value = self.squares[row][col]
        valid_moves = []
        
        if piece_value == 0:
            return valid_moves
        # enforce turn: only allow querying moves for side to move
        if int(piece_value) * self.side_to_move <= 0:
            return valid_moves
            
        piece_type = abs(piece_value)
        # Pawn (1)
        if piece_type == 1:
            valid_moves = Piece.get_pawn_moves(self, row, col, piece_value)   
        # Knight (2)
        if piece_type == 2:
            valid_moves = Piece.get_knight_moves(self, row, col, piece_value)
        # Bishop (3)
        if piece_type == 3:
            valid_moves = Piece.get_bishop_moves(self, row, col, piece_value)
        # Rook (4)
        if piece_type == 4:
            valid_moves = Piece.get_rook_moves(self, row, col, piece_value)      
        # Queen (5)
        if piece_type == 5:
            valid_moves = Piece.get_queen_moves(self, row, col, piece_value)
        # King (6)
        if piece_type == 6:
            # standard king moves
            valid_moves = Piece.get_king_moves(self, row, col, piece_value)

            color = 1 if piece_value > 0 else -1
            start_row = 7 if color == 1 else 0
            # castling
            king_not_moved = (not self.white_king_moved) if color == 1 else (not self.black_king_moved)
            if (row, col) == (start_row, 4) and not self.is_in_check(color) and king_not_moved:
                # Kingside
                if int(self.squares[start_row][7]) == 4 * color:
                    rook_kingside_not_moved = (not self.white_rook_kingside_moved) if color == 1 else (not self.black_rook_kingside_moved)
                    if rook_kingside_not_moved and int(self.squares[start_row][5]) == 0 and int(self.squares[start_row][6]) == 0:
                        if (not self.is_square_attacked(start_row, 5, -color)) and (not self.is_square_attacked(start_row, 6, -color)):
                            valid_moves.append((start_row, 6))
                # Queenside
                if int(self.squares[start_row][0]) == 4 * color:
                    rook_queenside_not_moved = (not self.white_rook_queenside_moved) if color == 1 else (not self.black_rook_queenside_moved)
                    if rook_queenside_not_moved and int(self.squares[start_row][1]) == 0 and int(self.squares[start_row][2]) == 0 and int(self.squares[start_row][3]) == 0:
                        if (not self.is_square_attacked(start_row, 3, -color)) and (not self.is_square_attacked(start_row, 2, -color)):
                            valid_moves.append((start_row, 2))


        # Filter out moves that would leave own king in check
        legal_moves = []
        color = 1 if piece_value > 0 else -1

        # Snapshot flags we need to restore
        for mv in valid_moves:
            saved_squares = self.squares.copy()
            saved_en_passant = getattr(self, 'en_passant_target', None)
            saved_flags = (
                self.white_king_moved,
                self.black_king_moved,
                self.white_rook_kingside_moved,
                self.white_rook_queenside_moved,
                self.black_rook_kingside_moved,
                self.black_rook_queenside_moved,
                self.side_to_move,
            )

            # Make the move
            self.move_piece((row, col), mv)

            if not self.is_in_check(color):
                legal_moves.append(mv)

            self.squares = saved_squares
            self.en_passant_target = saved_en_passant
            (
                self.white_king_moved,
                self.black_king_moved,
                self.white_rook_kingside_moved,
                self.white_rook_queenside_moved,
                self.black_rook_kingside_moved,
                self.black_rook_queenside_moved,
                self.side_to_move,
            ) = saved_flags

        return legal_moves

    def has_any_legal_moves(self, color):
        """Return True if side `color` (1 white, -1 black) has any legal moves."""
        saved_side = self.side_to_move
        self.side_to_move = color
        try:
            for r in range(8):
                for c in range(8):
                    if int(self.squares[r][c]) * color > 0:
                        moves = self.get_valid_moves(r, c)
                        if moves:
                            return True
            return False
        finally:
            self.side_to_move = saved_side
    

