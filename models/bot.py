import math
from abc import ABC, abstractmethod
import sys
import os

# Add src directory to path so we can import Board
SRC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src')
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from board import Board


class Bot(ABC):
    
    
    def __init__(self, color: int, depth: int = 3):
        """
        Initialize a bot.
        
        Args:
            color: 1 for white, -1 for black
            depth: search depth for the bot's algorithm
        """
        self.color = color
        self.depth = depth
    
    @abstractmethod
    def get_move(self, board: Board):
        """
        Get the best move for the current position.
        
        Args:
            board: The current board state
            
        Returns:
            A move tuple ((from_row, from_col), (to_row, to_col)) or None if no legal moves
        """
        pass


class AlphaBetaBot(Bot):
    """Bot using alpha-beta pruning algorithm"""
    
    PIECE_VALUES = {
        1: 100,   # pawn
        2: 320,   # knight
        3: 330,   # bishop
        4: 500,   # rook
        5: 900,   # queen
        6: 20000, # king
    }
    
    def __init__(self, color: int, depth: int = 3):
        """
        Initialize alpha-beta pruning bot.
        
        Args:
            color: 1 for white, -1 for black
            depth: search depth (default 3)
        """
        super().__init__(color, depth)
    
    def get_move(self, board: Board):
        _, move = self._alpha_beta(board, self.depth, -math.inf, math.inf)
        return move
    
    def _clone_board(self, board: Board) -> Board:
        """Create a deep copy of the board state"""
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
    
    def _generate_legal_moves(self, board: Board, color: int):
        """Generate all legal moves for a given color"""
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
    
    def _evaluate(self, board: Board) -> int:
        """
        Evaluate the board position from this bot's perspective.
        
        Args:
            board: The board state to evaluate
            
        Returns:
            A score (positive favors this bot, negative favors opponent)
        """
        # Terminal: checkmate or stalemate
        if not board.has_any_legal_moves(board.side_to_move):
            if board.is_in_check(board.side_to_move):
                # side_to_move is checkmated
                return -self.PIECE_VALUES[6] if board.side_to_move == self.color else self.PIECE_VALUES[6]
            return 0

        material = 0
        for r in range(8):
            for c in range(8):
                val = int(board.squares[r][c])
                if val != 0:
                    material += self.PIECE_VALUES[abs(val)] * (1 if val > 0 else -1)

        # score from bot perspective
        return material if self.color == 1 else -material
    
    def _alpha_beta(self, board: Board, depth: int, alpha: float, beta: float):
        """
        Alpha-beta pruning algorithm.
        
        Args:
            board: Current board state
            depth: Remaining depth to search
            alpha: Best score found for maximizer
            beta: Best score found for minimizer
            
        Returns:
            Tuple of (best_score, best_move)
        """
        if depth == 0:
            return self._evaluate(board), None

        legal_moves = self._generate_legal_moves(board, board.side_to_move)
        if not legal_moves:
            return self._evaluate(board), None

        maximizing = (board.side_to_move == self.color)

        best_move = None
        if maximizing:
            best_score = -math.inf
            for move in legal_moves:
                child = self._clone_board(board)
                child.move_piece(move[0], move[1])
                score, _ = self._alpha_beta(child, depth - 1, alpha, beta)
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
                child = self._clone_board(board)
                child.move_piece(move[0], move[1])
                score, _ = self._alpha_beta(child, depth - 1, alpha, beta)
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score, best_move


class RandomBot(Bot):
    """Bot that makes random legal moves"""
    
    def get_move(self, board: Board):
        import random
        legal_moves = self._get_legal_moves(board)
        return random.choice(legal_moves) if legal_moves else None
    
    def _get_legal_moves(self, board: Board):
        moves = []
        for r in range(8):
            for c in range(8):
                if int(board.squares[r][c]) * self.color > 0:
                    for mv in board.get_valid_moves(r, c):
                        moves.append(((r, c), mv))
        return moves


class CautiousBot(AlphaBetaBot):
    """More defensive playing style - heavily weights king safety"""
    
    def _evaluate(self, board: Board) -> int:
        base_eval = super()._evaluate(board)
        
        # Add king safety bonus/penalty
        king_safety = self._evaluate_king_safety(board)
        return base_eval + king_safety * 10
    
    def _evaluate_king_safety(self, board: Board) -> int:
        # Evaluate how safe each king is
        # Positive = good for this bot
        score = 0
        # ... implement king safety logic ...
        return score


class AggressiveBot(AlphaBetaBot):
    """Aggressive playing style - prioritizes piece capture and attacks"""
    
    def _evaluate(self, board: Board) -> int:
        base_eval = super()._evaluate(board)
        
        # Add attack bonus
        attack_bonus = self._count_attacked_pieces(board)
        return base_eval + attack_bonus * 5
    
    def _count_attacked_pieces(self, board: Board) -> int:
        # Count opponent pieces under attack
        # ... implement attack counting logic ...
        return 0        
    
class TacticalBot(AlphaBetaBot):
    """Bot that recognizes basic tactical patterns"""
    
    def get_move(self, board: Board):
        # First check for checkmate or winning tactics
        winning_move = self._find_checkmate(board)
        if winning_move:
            return winning_move
        
        # Then use normal alpha-beta
        _, move = self._alpha_beta(board, self.depth, -math.inf, math.inf)
        return move
    
    def _find_checkmate(self, board: Board):
        """Look for immediate checkmate moves"""
        legal_moves = self._generate_legal_moves(board, self.color)
        for move in legal_moves:
            child = self._clone_board(board)
            child.move_piece(move[0], move[1])
            if not child.has_any_legal_moves(-self.color):
                if child.is_in_check(-self.color):
                    return move
        return None