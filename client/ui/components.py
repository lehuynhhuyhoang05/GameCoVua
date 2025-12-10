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
    """Chess game timer widget - Enhanced"""
    
    def __init__(self, parent, initial_time=600):
        """
        Initialize timer
        
        Args:
            parent: Parent widget
            initial_time: Initial time in seconds (default 10 minutes)
        """
        super().__init__(parent, bg=COLORS['bg_card'], relief='solid', borderwidth=1, padx=15, pady=10)
        
        self.time_remaining = initial_time
        self.running = False
        self.timer_id = None
        
        # Timer display with gradient-like effect
        self.time_label = tk.Label(
            self,
            text=self._format_time(initial_time),
            font=FONTS['timer'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_dark']
        )
        self.time_label.pack(pady=5)
        
        # Status indicator with icons
        self.status_label = tk.Label(
            self,
            text="⏸ Ready",
            font=FONTS['small'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_muted']
        )
        self.status_label.pack()
        
        # Progress indicator (optional visual)
        self.initial_time = initial_time
    
    def _format_time(self, seconds):
        """Format seconds as MM:SS"""
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"
    
    def start(self):
        """Start timer with visual feedback"""
        if not self.running:
            self.running = True
            self.status_label.config(
                text="▶ Running",
                fg=COLORS['success']
            )
            self.config(bg=COLORS['bg_card'], borderwidth=2)
            self._tick()
    
    def pause(self):
        """Pause timer"""
        self.running = False
        self.status_label.config(
            text="⏸ Paused",
            fg=COLORS['text_muted']
        )
        self.config(borderwidth=1)
        if self.timer_id:
            self.after_cancel(self.timer_id)
    
    def _tick(self):
        """Timer tick with color transitions"""
        if self.running and self.time_remaining > 0:
            self.time_remaining -= 1
            self.time_label.config(text=self._format_time(self.time_remaining))
            
            # Dynamic color changes based on time
            if self.time_remaining <= 10:
                # Critical - blinking effect
                self.time_label.config(fg=COLORS['danger'])
                self.config(bg='#FFE5E5')
            elif self.time_remaining <= 30:
                self.time_label.config(fg=COLORS['danger'])
                self.config(bg=COLORS['bg_card'])
            elif self.time_remaining <= 60:
                self.time_label.config(fg=COLORS['warning'])
            else:
                self.time_label.config(fg=COLORS['text_dark'])
            
            self.timer_id = self.after(1000, self._tick)
        elif self.time_remaining == 0:
            self.status_label.config(
                text="⏰ Time's Up!",
                fg=COLORS['danger']
            )
            self.config(bg='#FFE5E5')
    
    def reset(self, time=600):
        """Reset timer"""
        self.pause()
        self.time_remaining = time
        self.time_label.config(
            text=self._format_time(time),
            fg=COLORS['text_dark']
        )


class MoveHistory(tk.Frame):
    """Move history display widget - Enhanced"""
    
    def __init__(self, parent):
        """Initialize move history"""
        super().__init__(parent, bg=COLORS['bg_card'], relief='solid', borderwidth=1)
        
        # Title with icon
        title_frame = tk.Frame(self, bg=COLORS['bg_card'])
        title_frame.pack(fill=tk.X, padx=10, pady=8)
        
        tk.Label(
            title_frame,
            text="📜",
            font=('Segoe UI', 16),
            bg=COLORS['bg_card']
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            title_frame,
            text="Move History",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_dark']
        ).pack(side=tk.LEFT)
        
        # Separator
        sep_frame = tk.Frame(self, bg=COLORS['bg_secondary'], height=1)
        sep_frame.pack(fill=tk.X)
        
        # Scrollbar and Listbox
        scroll_frame = tk.Frame(self, bg=COLORS['bg_card'])
        scroll_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.move_list = tk.Listbox(
            scroll_frame,
            font=('Consolas', 11),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_dark'],
            selectbackground=COLORS['primary'],
            selectforeground=COLORS['text_light'],
            yscrollcommand=scrollbar.set,
            height=12,
            width=18,
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0
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
        super().__init__(parent, bg=COLORS['bg_card'], relief='solid', borderwidth=1, padx=10, pady=10)
        
        self.color = color
        self.captured = []
        
        # Pieces display with wrapping
        self.pieces_label = tk.Label(
            self,
            text="No pieces captured yet",
            font=('Arial Unicode MS', 20),
            bg=COLORS['bg_card'],
            fg=COLORS['text_dark'],
            wraplength=180,
            justify='center'
        )
        self.pieces_label.pack(pady=5)
        
        # Point advantage
        self.points_label = tk.Label(
            self,
            text="Material: +0",
            font=FONTS['body_bold'],
            bg=COLORS['bg_card'],
            fg=COLORS['success']
        )
        self.points_label.pack(pady=(5, 0))
    
    def add_piece(self, piece: str):
        """Add captured piece"""
        self.captured.append(piece)
        self._update_display()
    
    def set_pieces(self, pieces: list):
        """Set all captured pieces"""
        self.captured = pieces.copy()
        self._update_display()
    
    def _update_display(self):
        """Update pieces display"""
        from ui.styles import PIECES_UNICODE
        
        if not self.captured:
            self.pieces_label.config(text="No pieces yet", fg=COLORS['text_muted'])
            self.points_label.config(text="Material: +0", fg=COLORS['text_gray'])
            return
        
        # Sort pieces by value
        piece_order = {'q': 5, 'r': 4, 'b': 3, 'n': 2, 'p': 1,
                      'Q': 5, 'R': 4, 'B': 3, 'N': 2, 'P': 1}
        sorted_pieces = sorted(self.captured, key=lambda p: piece_order.get(p, 0), reverse=True)
        
        # Display pieces with spacing
        piece_text = '  '.join([PIECES_UNICODE.get(p, p) for p in sorted_pieces])
        self.pieces_label.config(text=piece_text, fg=COLORS['text_dark'])
        
        # Calculate point advantage
        piece_values = {'q': 9, 'r': 5, 'b': 3, 'n': 3, 'p': 1,
                       'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'P': 1}
        points = sum(piece_values.get(p, 0) for p in sorted_pieces)
        
        # Color based on advantage
        color = COLORS['success'] if points > 0 else COLORS['text_dark']
        self.points_label.config(text=f"Material: +{points}", fg=color)
    
    def clear(self):
        """Clear captured pieces"""
        self.captured.clear()
        self._update_display()


class PlayerInfo(tk.Frame):
    """Player information display - Enhanced with active state animation"""
    
    def __init__(self, parent, username="Player", color="white", rating=1200):
        """Initialize player info"""
        super().__init__(
            parent,
            bg=COLORS['bg_card'],
            relief='solid',
            borderwidth=2,
            padx=12,
            pady=10
        )
        
        self.username = username
        self.color = color
        self.rating = rating
        self.is_active = False
        
        # Container
        container = tk.Frame(self, bg=COLORS['bg_card'])
        container.pack(fill=tk.BOTH, expand=True)
        
        # Color indicator with better styling
        color_bg = COLORS['bg_card']
        if color == "white":
            color_symbol = "⚪"
            color_text = "White"
        else:
            color_symbol = "⚫"
            color_text = "Black"
        
        color_frame = tk.Frame(container, bg=color_bg, width=50)
        color_frame.pack(side=tk.LEFT, padx=(0, 10))
        color_frame.pack_propagate(False)
        
        self.color_label = tk.Label(
            color_frame,
            text=color_symbol,
            font=('Segoe UI', 24),
            bg=color_bg
        )
        self.color_label.pack(expand=True)
        
        # Info section
        info_frame = tk.Frame(container, bg=COLORS['bg_card'])
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Username
        self.username_label = tk.Label(
            info_frame,
            text=username,
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_dark'],
            anchor='w'
        )
        self.username_label.pack(anchor='w', fill=tk.X)
        
        # Color and rating in one line
        details_frame = tk.Frame(info_frame, bg=COLORS['bg_card'])
        details_frame.pack(anchor='w', fill=tk.X)
        
        tk.Label(
            details_frame,
            text=f"{color_text} • ",
            font=FONTS['small'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_muted']
        ).pack(side=tk.LEFT)
        
        self.rating_label = tk.Label(
            details_frame,
            text=f"⭐ {rating}",
            font=FONTS['small'],
            bg=COLORS['bg_card'],
            fg=COLORS['warning']
        )
        self.rating_label.pack(side=tk.LEFT)
    
    def set_active(self, active=True):
        """Set player as active (their turn) with animated border"""
        self.is_active = active
        
        if active:
            # Active state - glowing effect
            self.config(
                bg='#E8F5E9',  # Light green background
                borderwidth=3,
                relief='solid'
            )
            
            # Update all child backgrounds
            for widget in self.winfo_children():
                if isinstance(widget, (tk.Frame, tk.Label)):
                    widget.config(bg='#E8F5E9')
                    for child in widget.winfo_children():
                        if isinstance(child, (tk.Frame, tk.Label)):
                            child.config(bg='#E8F5E9')
            
            # Add glow effect via border color (simulated)
            self.config(highlightbackground=COLORS['success'], highlightthickness=2)
        else:
            # Inactive state
            self.config(
                bg=COLORS['bg_card'],
                borderwidth=2,
                relief='solid',
                highlightthickness=0
            )
            
            # Restore backgrounds
            for widget in self.winfo_children():
                if isinstance(widget, (tk.Frame, tk.Label)):
                    widget.config(bg=COLORS['bg_card'])
                    for child in widget.winfo_children():
                        if isinstance(child, (tk.Frame, tk.Label)):
                            child.config(bg=COLORS['bg_card'])
