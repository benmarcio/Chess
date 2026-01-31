#!/usr/bin/env python3
"""Quick test to verify PGN save functionality"""

import sys
import os

# Add parent directory to path
ROOT_DIR = os.path.dirname(__file__)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from src.board import Board
from models.alphabeta_bot import choose_move

def test_bot_vs_bot_pgn_save():
    """Test bot vs bot game and PGN save"""
    board = Board()
    moves = []
    max_moves = 50  # Limit to 50 moves to prevent infinite games
    
    print("Starting bot vs bot test game...")
    
    for move_num in range(max_moves):
        move = choose_move(board, board.side_to_move, depth=3)
        if move is None:
            print(f"No move found for {board.side_to_move}")
            break
        
        (sr, sc), (fr, fc) = move
        
        # Convert to algebraic
        files = 'abcdefgh'
        ranks = '87654321'
        from_sq = files[sc] + ranks[sr]
        to_sq = files[fc] + ranks[fr]
        
        print(f"Move {move_num+1}: {from_sq}{to_sq}")
        moves.append(move)
        board.move_piece((sr, sc), (fr, fc))
        
        # Check for game over
        if not board.has_any_legal_moves(board.side_to_move):
            if board.is_in_check(board.side_to_move):
                winner = 'White' if board.side_to_move == -1 else 'Black'
                print(f"Game Over: {winner} wins by checkmate")
            else:
                print(f"Game Over: Draw (stalemate)")
            break
    
    print(f"Total moves: {len(moves)}")
    
    # Now test PGN generation
    try:
        import chess
        import chess.pgn
        
        game = chess.pgn.Game()
        game.headers["Event"] = "Live Chess"
        game.headers["Site"] = "Chess.com"
        game.headers["Date"] = "2026.01.31"
        game.headers["White"] = "Bot"
        game.headers["Black"] = "Bot"
        game.headers["Result"] = "1-0"
        
        board = chess.Board()
        node = game
        
        for move in moves:
            from_pos, to_pos = move
            from_sq = f"{files[from_pos[1]]}{ranks[from_pos[0]]}"
            to_sq = f"{files[to_pos[1]]}{ranks[to_pos[0]]}"
            uci = f"{from_sq}{to_sq}"
            
            try:
                chess_move = chess.Move.from_uci(uci)
                if chess_move not in board.legal_moves:
                    print(f"Illegal move: {uci}")
                    break
                node = node.add_variation(chess_move)
                board.push(chess_move)
            except Exception as e:
                print(f"Error with move {uci}: {e}")
                break
        
        exporter = chess.pgn.StringExporter(headers=True, variations=False, comments=False)
        pgn_text = game.accept(exporter).strip()
        
        print(f"\nGenerated PGN:\n{pgn_text[:200]}...")
        
        # Try to save
        pgn_path = os.path.join(ROOT_DIR, 'data', 'test_game.pgn')
        os.makedirs(os.path.dirname(pgn_path), exist_ok=True)
        
        with open(pgn_path, 'w', encoding='utf-8') as f:
            f.write(pgn_text)
            f.write('\n\n')
        
        print(f"\nSaved to {pgn_path}")
        
        # Verify file exists and has content
        if os.path.exists(pgn_path):
            with open(pgn_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"File verification: {len(content)} bytes written")
        else:
            print("ERROR: File was not created!")
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_bot_vs_bot_pgn_save()
