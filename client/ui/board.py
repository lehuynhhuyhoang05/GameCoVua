"""
Chess Board UI using Tkinter
"""

import tkinter as tk
from tkinter import Canvas
from typing import Optional, Callable, List, Tuple
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.styles import COLORS, FONTS, PIECES_UNICODE


# Chess piece Unicode symbols
PIECES = PIECES_UNICODE

# Colors
LIGHT_SQUARE = COLORS['light_square']
DARK_SQUARE = COLORS['dark_square']
HIGHLIGHT_COLOR = COLORS['legal_move']
SELECTED_COLOR = COLORS['selected']
LAST_MOVE_COLOR = COLORS['last_move']
CHECK_COLOR = COLORS['check']


class ChessBoardUI:
    """Chess board visual representation"""
    
    def __init__(self, parent, size=560, flipped=False):
        """
        Initialize chess board
        
        Args:
            parent: Parent tkinter widget
            size: Board size in pixels
            flipped: True if board should be flipped (black perspective)
        """
        self.parent = parent
        self.size = size
        self.square_size = size // 8
        self.flipped = flipped
        
        self.canvas = Canvas(parent, width=size, height=size, bg='white', highlightthickness=0)
        self.canvas.pack()
        
        self.selected_square: Optional[tuple] = None
        self.highlighted_squares: List[tuple] = []
        self.last_move: Optional[Tuple[tuple, tuple]] = None
        self.check_square: Optional[tuple] = None
        self.pieces: dict = {}  # (row, col) -> piece symbol
        
        self.click_callback: Optional[Callable] = None
        self.hover_square: Optional[tuple] = None
        
        self.canvas.bind('<Button-1>', self._on_click)
        self.canvas.bind('<Motion>', self._on_hover)
        
        self.draw_board()
    
    def draw_board(self):
        """Draw the chess board squares"""
        self.canvas.delete('all')
        
        for row in range(8):
            for col in range(8):
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                
                # Determine square color
                is_light = (row + col) % 2 == 0
                color = LIGHT_SQUARE if is_light else DARK_SQUARE
                
                # Highlight last move
                if self.last_move and ((row, col) == self.last_move[0] or (row, col) == self.last_move[1]):
                    color = LAST_MOVE_COLOR
                # Highlight if selected
                elif (row, col) == self.selected_square:
                    color = SELECTED_COLOR
                # Highlight legal moves
                elif (row, col) in self.highlighted_squares:
                    color = HIGHLIGHT_COLOR
                # Highlight check
                elif (row, col) == self.check_square:
                    color = CHECK_COLOR
                
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline='',
                    tags='square'
                )
        
        # Draw coordinates
        for i in range(8):
            # Files (a-h)
            file_label = chr(ord('a') + i) if not self.flipped else chr(ord('h') - i)
            self.canvas.create_text(
                i * self.square_size + self.square_size // 2,
                self.size - 10,
                text=file_label,
                font=FONTS['board_coord'],
                fill=COLORS['text_gray'],
                tags='coords'
            )
            
            # Ranks (1-8)
            rank_label = str(8 - i) if not self.flipped else str(i + 1)
            self.canvas.create_text(
                10,
                i * self.square_size + self.square_size // 2,
                text=rank_label,
                font=FONTS['board_coord'],
                fill=COLORS['text_gray'],
                tags='coords'
            )
        
        self.draw_pieces()
    
    def draw_pieces(self):
        """Draw chess pieces on the board"""
        self.canvas.delete('piece')
        
        for (row, col), piece in self.pieces.items():
            if piece:
                x = col * self.square_size + self.square_size // 2
                y = row * self.square_size + self.square_size // 2
                
                symbol = PIECES.get(piece, piece)
                piece_size = self.square_size // 2 + 10
                
                self.canvas.create_text(
                    x, y,
                    text=symbol,
                    font=('Arial', piece_size, 'bold'),
                    tags='piece'
                )
    
    def set_last_move(self, from_square: str, to_square: str):
        """Highlight the last move made"""
        self.last_move = (
            self.square_to_coords(from_square),
            self.square_to_coords(to_square)
        )
        self.draw_board()
    
    def set_check_square(self, square: Optional[str]):
        """Highlight square in check"""
        if square:
            self.check_square = self.square_to_coords(square)
        else:
            self.check_square = None
        self.draw_board()
    
    def _on_hover(self, event):
        """Handle mouse hover"""
        col = event.x // self.square_size
        row = event.y // self.square_size
        
        if 0 <= row < 8 and 0 <= col < 8:
            self.hover_square = (row, col)
            # Could add hover effect here
        else:
            self.hover_square = None
    
    def set_position(self, fen: str):
        """
        Set board position from FEN string
        
        Args:
            fen: FEN string representing board position
        """
        self.pieces.clear()
        
        # Parse FEN (only the board part)
        board_fen = fen.split()[0]
        ranks = board_fen.split('/')
        
        for row, rank in enumerate(ranks):
            col = 0
            for char in rank:
                if char.isdigit():
                    col += int(char)
                else:
                    display_row = row if not self.flipped else 7 - row
                    display_col = col if not self.flipped else 7 - col
                    self.pieces[(display_row, display_col)] = char
                    col += 1
        
        self.draw_pieces()
    
    def select_square(self, row: int, col: int):
        """Select a square"""
        self.selected_square = (row, col)
        self.draw_board()
    
    def clear_selection(self):
        """Clear square selection"""
        self.selected_square = None
        self.highlighted_squares.clear()
        self.draw_board()
    
    def highlight_squares(self, squares: List[tuple]):
        """Highlight specific squares"""
        self.highlighted_squares = squares
        self.draw_board()
    
    def _on_click(self, event):
        """Handle mouse click on board"""
        col = event.x // self.square_size
        row = event.y // self.square_size
        
        if 0 <= row < 8 and 0 <= col < 8:
            if self.click_callback:
                self.click_callback(row, col)
    
    def set_click_callback(self, callback: Callable):
        """Set callback for square clicks"""
        self.click_callback = callback
    
    def coords_to_square(self, row: int, col: int) -> str:
        """Convert board coordinates to chess notation"""
        if self.flipped:
            file = chr(ord('h') - col)
            rank = str(row + 1)
        else:
            file = chr(ord('a') + col)
            rank = str(8 - row)
        return file + rank
    
    def square_to_coords(self, square: str) -> tuple:
        """Convert chess notation to board coordinates"""
        file = square[0]
        rank = square[1]
        
        if self.flipped:
            col = ord('h') - ord(file)
            row = int(rank) - 1
        else:
            col = ord(file) - ord('a')
            row = 8 - int(rank)
        
        return (row, col)
    
    def flip_board(self):
        """Flip board perspective"""
        self.flipped = not self.flipped
        # Redraw with current position
        current_fen = self._get_current_fen()
        self.set_position(current_fen)
    
    def _get_current_fen(self) -> str:
        """Get FEN from current piece positions (simplified)"""
        fen_rows = []
        for row in range(8):
            fen_row = ""
            empty_count = 0
            for col in range(8):
                piece = self.pieces.get((row, col))
                if piece:
                    if empty_count > 0:
                        fen_row += str(empty_count)
                        empty_count = 0
                    fen_row += piece
                else:
                    empty_count += 1
            if empty_count > 0:
                fen_row += str(empty_count)
            fen_rows.append(fen_row)
        return '/'.join(fen_rows) + ' w KQkq - 0 1'
