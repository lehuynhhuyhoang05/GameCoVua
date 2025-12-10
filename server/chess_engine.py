"""
Chess Engine using python-chess library
Handles game logic, move validation, and game state
"""

import chess
from typing import Optional, List, Tuple


class ChessEngine:
    """Chess game engine with full rule implementation"""
    
    def __init__(self):
        """Initialize chess board with starting position"""
        self.board = chess.Board()
        self.move_history = []
        self.captured_by_white = []  # Pieces captured by white
        self.captured_by_black = []  # Pieces captured by black
        
    def reset(self):
        """Reset board to starting position"""
        self.board.reset()
        self.move_history = []
        self.captured_by_white = []
        self.captured_by_black = []
        
    def make_move(self, from_square: str, to_square: str, promotion: str = None) -> bool:
        """
        Make a move on the board
        
        Args:
            from_square: Source square (e.g., 'e2')
            to_square: Destination square (e.g., 'e4')
            promotion: Promotion piece ('q', 'r', 'b', 'n') if pawn promotion
            
        Returns:
            True if move is valid and made, False otherwise
        """
        try:
            # Convert square notation to chess.Square
            from_sq = chess.parse_square(from_square)
            to_sq = chess.parse_square(to_square)
            
            # Create move
            if promotion:
                promotion_piece = {
                    'q': chess.QUEEN,
                    'r': chess.ROOK,
                    'b': chess.BISHOP,
                    'n': chess.KNIGHT
                }.get(promotion.lower())
                move = chess.Move(from_sq, to_sq, promotion=promotion_piece)
            else:
                move = chess.Move(from_sq, to_sq)
            
            # Check if move is legal
            if move in self.board.legal_moves:
                # Check if this is a capture
                captured_piece = None
                if self.board.is_capture(move):
                    # Get the piece at destination
                    piece_at_dest = self.board.piece_at(to_sq)
                    if piece_at_dest:
                        # Convert to FEN notation
                        captured_piece = piece_at_dest.symbol()
                        # Add to appropriate capture list
                        if self.board.turn == chess.WHITE:
                            self.captured_by_white.append(captured_piece)
                        else:
                            self.captured_by_black.append(captured_piece)
                
                self.board.push(move)
                self.move_history.append(move)
                return True, captured_piece
            return False, None
            
        except (ValueError, chess.InvalidMoveError):
            return False, None
    
    def is_valid_move(self, from_square: str, to_square: str) -> bool:
        """Check if a move is legal"""
        try:
            from_sq = chess.parse_square(from_square)
            to_sq = chess.parse_square(to_square)
            move = chess.Move(from_sq, to_sq)
            return move in self.board.legal_moves
        except ValueError:
            return False
    
    def get_legal_moves(self, square: str) -> List[str]:
        """Get all legal moves for a piece at given square"""
        try:
            sq = chess.parse_square(square)
            moves = []
            for move in self.board.legal_moves:
                if move.from_square == sq:
                    moves.append(chess.square_name(move.to_square))
            return moves
        except ValueError:
            return []
    
    def get_piece_at(self, square: str) -> Optional[str]:
        """Get piece symbol at given square"""
        try:
            sq = chess.parse_square(square)
            piece = self.board.piece_at(sq)
            return piece.symbol() if piece else None
        except ValueError:
            return None
    
    def get_piece_color(self, square: str) -> Optional[str]:
        """Get color of piece at given square"""
        try:
            sq = chess.parse_square(square)
            piece = self.board.piece_at(sq)
            if piece:
                return "white" if piece.color == chess.WHITE else "black"
            return None
        except ValueError:
            return None
    
    def is_check(self) -> bool:
        """Check if current player is in check"""
        return self.board.is_check()
    
    def is_checkmate(self) -> bool:
        """Check if current player is in checkmate"""
        return self.board.is_checkmate()
    
    def is_stalemate(self) -> bool:
        """Check if game is in stalemate"""
        return self.board.is_stalemate()
    
    def is_game_over(self) -> bool:
        """Check if game is over"""
        return self.board.is_game_over()
    
    def get_game_result(self) -> Optional[str]:
        """Get game result"""
        if self.board.is_checkmate():
            return "black_win" if self.board.turn == chess.WHITE else "white_win"
        elif self.board.is_stalemate():
            return "draw"
        elif self.board.is_insufficient_material():
            return "draw"
        return None
    
    def get_current_turn(self) -> str:
        """Get current turn color"""
        return "white" if self.board.turn == chess.WHITE else "black"
    
    def get_board_state(self) -> str:
        """Get FEN representation of board"""
        return self.board.fen()
    
    def set_board_state(self, fen: str) -> bool:
        """Set board from FEN string"""
        try:
            self.board.set_fen(fen)
            return True
        except ValueError:
            return False
    
    def get_move_history(self) -> List[str]:
        """Get move history in SAN notation"""
        return [self.board.san(move) for move in self.move_history]
    
    def undo_move(self) -> bool:
        """Undo last move"""
        try:
            self.board.pop()
            if self.move_history:
                self.move_history.pop()
            return True
        except IndexError:
            return False
