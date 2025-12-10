"""
Additional UI components: Timer, Move History, Captured Pieces
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.styles import COLORS, FONTS


class ChessTimer(tk.Frame):
    """Chess game timer widget"""
    
    def __init__(self, parent, initial_time=600):
        """
        Initialize timer
        
        Args:
            parent: Parent widget
            initial_time: Initial time in seconds (default 10 minutes)
        """
        super().__init__(parent, bg=COLORS['bg_primary'])
        
        self.time_remaining = initial_time
        self.running = False
        self.timer_id = None
        
        # Timer display
        self.time_label = tk.Label(
            self,
            text=self._format_time(initial_time),
            font=('Digital-7', 32, 'bold'),
            bg=COLORS['bg_primary'],
            fg=COLORS['text_dark']
        )
        self.time_label.pack(pady=5)
        
        # Status indicator
        self.status_label = tk.Label(
            self,
            text="⏸ Paused",
            font=FONTS['small'],
            bg=COLORS['bg_primary'],
            fg=COLORS['text_gray']
        )
        self.status_label.pack()
    
    def _format_time(self, seconds):
        """Format seconds as MM:SS"""
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"
    
    def start(self):
        """Start timer"""
        if not self.running:
            self.running = True
            self.status_label.config(text="▶ Running", fg=COLORS['success'])
            self._tick()
    
    def pause(self):
        """Pause timer"""
        self.running = False
        self.status_label.config(text="⏸ Paused", fg=COLORS['text_gray'])
        if self.timer_id:
            self.after_cancel(self.timer_id)
    
    def _tick(self):
        """Timer tick"""
        if self.running and self.time_remaining > 0:
            self.time_remaining -= 1
            self.time_label.config(text=self._format_time(self.time_remaining))
            
            # Change color when time is low
            if self.time_remaining <= 30:
                self.time_label.config(fg=COLORS['danger'])
            elif self.time_remaining <= 60:
                self.time_label.config(fg=COLORS['warning'])
            
            self.timer_id = self.after(1000, self._tick)
        elif self.time_remaining == 0:
            self.status_label.config(text="⏰ Time's Up!", fg=COLORS['danger'])
    
    def reset(self, time=600):
        """Reset timer"""
        self.pause()
        self.time_remaining = time
        self.time_label.config(
            text=self._format_time(time),
            fg=COLORS['text_dark']
        )


class MoveHistory(tk.Frame):
    """Move history display widget"""
    
    def __init__(self, parent):
        """Initialize move history"""
        super().__init__(parent, bg=COLORS['bg_primary'])
        
        # Title
        tk.Label(
            self,
            text="📜 Move History",
            font=FONTS['subheading'],
            bg=COLORS['bg_primary'],
            fg=COLORS['text_dark']
        ).pack(pady=5)
        
        # Scrollbar and Listbox
        scroll_frame = tk.Frame(self, bg=COLORS['bg_primary'])
        scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.move_list = tk.Listbox(
            scroll_frame,
            font=('Courier New', 10),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_dark'],
            selectbackground=COLORS['primary'],
            selectforeground=COLORS['text_light'],
            yscrollcommand=scrollbar.set,
            height=15,
            width=20,
            relief=tk.FLAT,
            borderwidth=0
        )
        self.move_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.move_list.yview)
        
        self.moves = []
        self.move_number = 1
    
    def add_move(self, move: str, color: str):
        """Add move to history"""
        if color == "white":
            move_text = f"{self.move_number}. {move}"
            self.moves.append(move_text)
            self.move_list.insert(tk.END, move_text)
        else:
            move_text = f"   {move}"
            if self.moves:
                self.moves[-1] += f" {move}"
                self.move_list.delete(tk.END)
                self.move_list.insert(tk.END, self.moves[-1])
            self.move_number += 1
        
        self.move_list.see(tk.END)
    
    def clear(self):
        """Clear move history"""
        self.move_list.delete(0, tk.END)
        self.moves.clear()
        self.move_number = 1


class CapturedPieces(tk.Frame):
    """Display captured pieces"""
    
    def __init__(self, parent, color="white"):
        """Initialize captured pieces display"""
        super().__init__(parent, bg=COLORS['bg_primary'])
        
        self.color = color
        self.captured = []
        
        # Title
        title_text = f"Captured by {color.capitalize()}"
        tk.Label(
            self,
            text=title_text,
            font=FONTS['small'],
            bg=COLORS['bg_primary'],
            fg=COLORS['text_gray']
        ).pack()
        
        # Pieces display
        self.pieces_label = tk.Label(
            self,
            text="",
            font=('Arial', 16),
            bg=COLORS['bg_primary'],
            fg=COLORS['text_dark']
        )
        self.pieces_label.pack()
        
        # Point advantage
        self.points_label = tk.Label(
            self,
            text="+0",
            font=FONTS['small'],
            bg=COLORS['bg_primary'],
            fg=COLORS['success']
        )
        self.points_label.pack()
    
    def add_piece(self, piece: str):
        """Add captured piece"""
        self.captured.append(piece)
        self._update_display()
    
    def _update_display(self):
        """Update pieces display"""
        from ui.styles import PIECES_UNICODE
        
        # Sort pieces by value
        piece_order = {'q': 5, 'r': 4, 'b': 3, 'n': 2, 'p': 1,
                      'Q': 5, 'R': 4, 'B': 3, 'N': 2, 'P': 1}
        sorted_pieces = sorted(self.captured, key=lambda p: piece_order.get(p, 0), reverse=True)
        
        # Display pieces
        piece_text = ' '.join([PIECES_UNICODE.get(p, p) for p in sorted_pieces])
        self.pieces_label.config(text=piece_text)
        
        # Calculate point advantage
        piece_values = {'q': 9, 'r': 5, 'b': 3, 'n': 3, 'p': 1,
                       'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'P': 1}
        points = sum(piece_values.get(p, 0) for p in sorted_pieces)
        self.points_label.config(text=f"+{points}")
    
    def clear(self):
        """Clear captured pieces"""
        self.captured.clear()
        self._update_display()


class PlayerInfo(tk.Frame):
    """Player information display"""
    
    def __init__(self, parent, username="Player", color="white", rating=1200):
        """Initialize player info"""
        super().__init__(parent, bg=COLORS['bg_secondary'], relief=tk.SOLID, borderwidth=1)
        
        self.username = username
        self.color = color
        self.rating = rating
        
        # Container
        container = tk.Frame(self, bg=COLORS['bg_secondary'])
        container.pack(padx=10, pady=8, fill=tk.BOTH, expand=True)
        
        # Color indicator
        color_symbol = "⚪" if color == "white" else "⚫"
        self.color_label = tk.Label(
            container,
            text=color_symbol,
            font=('Arial', 20),
            bg=COLORS['bg_secondary']
        )
        self.color_label.pack(side=tk.LEFT, padx=5)
        
        # Info
        info_frame = tk.Frame(container, bg=COLORS['bg_secondary'])
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.username_label = tk.Label(
            info_frame,
            text=username,
            font=FONTS['subheading'],
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_dark'],
            anchor='w'
        )
        self.username_label.pack(anchor='w')
        
        self.rating_label = tk.Label(
            info_frame,
            text=f"Rating: {rating}",
            font=FONTS['small'],
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_gray'],
            anchor='w'
        )
        self.rating_label.pack(anchor='w')
    
    def set_active(self, active=True):
        """Set player as active (their turn)"""
        if active:
            self.config(bg=COLORS['success'], borderwidth=2)
            for widget in self.winfo_children():
                widget.config(bg=COLORS['success'])
                for child in widget.winfo_children():
                    child.config(bg=COLORS['success'])
        else:
            self.config(bg=COLORS['bg_secondary'], borderwidth=1)
            for widget in self.winfo_children():
                widget.config(bg=COLORS['bg_secondary'])
                for child in widget.winfo_children():
                    child.config(bg=COLORS['bg_secondary'])
