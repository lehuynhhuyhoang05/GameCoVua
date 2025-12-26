"""
AI opponent using Stockfish or simple minimax
"""

import chess
import chess.engine
import random
from typing import Optional
import os


class ChessAI:
    """Chess AI opponent"""
    
    def __init__(self, difficulty: str = 'medium'):
        """
        Initialize AI
        
        Args:
            difficulty: 'easy', 'medium', 'hard', or 'stockfish'
        """
        self.difficulty = difficulty
        self.stockfish_engine = None
        self.use_stockfish = False
        
        # Try to initialize Stockfish if available
        if difficulty == 'stockfish':
            self._init_stockfish()
    
    def _init_stockfish(self):
        """Try to initialize Stockfish engine"""
        try:
            # Common Stockfish paths
            stockfish_paths = [
                'stockfish',
                'stockfish.exe',
                '/usr/games/stockfish',
                '/usr/local/bin/stockfish',
                'C:\\Program Files\\Stockfish\\stockfish.exe',
                os.path.join(os.getcwd(), 'stockfish.exe')
            ]
            
            for path in stockfish_paths:
                try:
                    self.stockfish_engine = chess.engine.SimpleEngine.popen_uci(path)
                    self.use_stockfish = True
                    print(f"✅ Stockfish initialized from: {path}")
                    return
                except:
                    continue
            
            print("⚠️ Stockfish not found, falling back to minimax")
            self.difficulty = 'hard'
            
        except Exception as e:
            print(f"Stockfish initialization error: {e}")
            self.difficulty = 'hard'
    
    def get_move(self, board: chess.Board) -> Optional[chess.Move]:
        """
        Get AI move for current board position
        
        Args:
            board: Current chess board state
            
        Returns:
            Best move according to AI
        """
        if self.use_stockfish and self.stockfish_engine:
            return self._get_stockfish_move(board)
        elif self.difficulty == 'easy':
            return self._get_random_move(board)
        elif self.difficulty == 'medium':
            return self._get_minimax_move(board, depth=2)
        else:  # hard
            return self._get_minimax_move(board, depth=3)
    
    def _get_stockfish_move(self, board: chess.Board) -> Optional[chess.Move]:
        """Get move from Stockfish engine"""
        try:
            result = self.stockfish_engine.play(board, chess.engine.Limit(time=0.1))
            return result.move
        except:
            return self._get_minimax_move(board, depth=2)
    
    def _get_random_move(self, board: chess.Board) -> Optional[chess.Move]:
        """Get random legal move"""
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None
        return random.choice(legal_moves)
    
    def _get_minimax_move(self, board: chess.Board, depth: int = 2) -> Optional[chess.Move]:
        """Get move using minimax algorithm with alpha-beta pruning"""
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        for move in board.legal_moves:
            board.push(move)
            value = self._minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            
            if value > best_value:
                best_value = value
                best_move = move
            
            alpha = max(alpha, best_value)
        
        return best_move
    
    def _minimax(self, board: chess.Board, depth: int, alpha: float, 
                 beta: float, maximizing: bool) -> float:
        """Minimax algorithm with alpha-beta pruning"""
        if depth == 0 or board.is_game_over():
            return self._evaluate_board(board)
        
        if maximizing:
            max_eval = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                eval_score = self._minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval_score = self._minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval
    
    def _evaluate_board(self, board: chess.Board) -> float:
        """
        Evaluate board position
        
        Returns:
            Score from white's perspective (positive = white advantage)
        """
        if board.is_checkmate():
            return -10000 if board.turn else 10000
        
        if board.is_stalemate() or board.is_insufficient_material():
            return 0
        
        # Piece values
        piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }
        
        score = 0
        
        # Material count
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = piece_values.get(piece.piece_type, 0)
                score += value if piece.color == chess.WHITE else -value
        
        # Mobility (number of legal moves)
        mobility_score = len(list(board.legal_moves))
        score += mobility_score * 10 if board.turn == chess.WHITE else -mobility_score * 10
        
        # Center control
        center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
        for square in center_squares:
            piece = board.piece_at(square)
            if piece:
                score += 30 if piece.color == chess.WHITE else -30
        
        return score if board.turn == chess.WHITE else -score
    
    def close(self):
        """Clean up resources"""
        if self.stockfish_engine:
            try:
                self.stockfish_engine.quit()
            except:
                pass


class AIOpponent:
    """Wrapper for AI opponent with personality"""
    
    def __init__(self, name: str = "Computer", difficulty: str = 'medium'):
        self.name = name
        self.ai = ChessAI(difficulty)
        self.difficulty = difficulty
    
    def get_move(self, board: chess.Board) -> Optional[chess.Move]:
        """Get AI's move"""
        return self.ai.get_move(board)
    
    def get_personality_message(self, event: str) -> str:
        """Get personality-based message"""
        messages = {
            'game_start': [
                "Let's have a good game!",
                "May the best player win!",
                "Good luck, have fun!",
                "Ready when you are!"
            ],
            'good_move': [
                "Nice move!",
                "Well played!",
                "Interesting...",
                "I didn't see that coming!"
            ],
            'check': [
                "Check!",
                "Your king is in danger!",
                "Careful now...",
                "Watch your king!"
            ],
            'blunder': [
                "Are you sure about that?",
                "Hmm...",
                "Interesting choice...",
                "I'll take advantage of that!"
            ],
            'win': [
                "Good game!",
                "Better luck next time!",
                "That was fun!",
                "Thanks for the game!"
            ],
            'lose': [
                "Well played!",
                "You got me!",
                "Nice game!",
                "You're too good!"
            ]
        }
        
        return random.choice(messages.get(event, ["..."]))
    
    def close(self):
        """Clean up"""
        self.ai.close()
