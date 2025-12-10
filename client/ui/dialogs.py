"""
Custom dialogs for Chess game
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.styles import COLORS, FONTS, PIECES_UNICODE, get_button_style


class PawnPromotionDialog(tk.Toplevel):
    """Beautiful pawn promotion selection dialog"""
    
    def __init__(self, parent, color="white"):
        """
        Initialize pawn promotion dialog
        
        Args:
            parent: Parent window
            color: Piece color ("white" or "black")
        """
        super().__init__(parent)
        
        self.result = None
        self.color = color
        
        # Window setup
        self.title("Pawn Promotion")
        self.resizable(False, False)
        self.configure(bg=COLORS['bg_primary'])
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Center window
        self.update_idletasks()
        width = 400
        height = 300
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create dialog widgets"""
        # Title
        title_frame = tk.Frame(self, bg=COLORS['primary'], pady=15)
        title_frame.pack(fill=tk.X)
        
        tk.Label(
            title_frame,
            text="♟️ Pawn Promotion",
            font=FONTS['heading'],
            bg=COLORS['primary'],
            fg=COLORS['text_light']
        ).pack()
        
        tk.Label(
            title_frame,
            text="Choose your piece",
            font=FONTS['small'],
            bg=COLORS['primary'],
            fg=COLORS['text_light']
        ).pack()
        
        # Main content
        content_frame = tk.Frame(self, bg=COLORS['bg_primary'], padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Piece selection buttons
        pieces_frame = tk.Frame(content_frame, bg=COLORS['bg_primary'])
        pieces_frame.pack(expand=True)
        
        # Define pieces
        if self.color == "white":
            pieces = [
                ('Q', '♕', 'Queen', 'The most powerful piece'),
                ('R', '♖', 'Rook', 'Strong and versatile'),
                ('B', '♗', 'Bishop', 'Moves diagonally'),
                ('N', '♘', 'Knight', 'Unique L-shaped moves'),
            ]
        else:
            pieces = [
                ('q', '♛', 'Queen', 'The most powerful piece'),
                ('r', '♜', 'Rook', 'Strong and versatile'),
                ('b', '♝', 'Bishop', 'Moves diagonally'),
                ('n', '♞', 'Knight', 'Unique L-shaped moves'),
            ]
        
        # Create buttons in 2x2 grid
        for i, (code, symbol, name, desc) in enumerate(pieces):
            row = i // 2
            col = i % 2
            
            btn_frame = tk.Frame(
                pieces_frame,
                bg=COLORS['bg_card'],
                relief='solid',
                borderwidth=1,
                padx=15,
                pady=15,
                cursor='hand2'
            )
            btn_frame.grid(row=row, column=col, padx=10, pady=10)
            
            # Piece symbol
            piece_label = tk.Label(
                btn_frame,
                text=symbol,
                font=('Arial Unicode MS', 48),
                bg=COLORS['bg_card'],
                fg=COLORS['text_dark']
            )
            piece_label.pack()
            
            # Piece name
            name_label = tk.Label(
                btn_frame,
                text=name,
                font=FONTS['body_bold'],
                bg=COLORS['bg_card'],
                fg=COLORS['text_dark']
            )
            name_label.pack()
            
            # Description
            desc_label = tk.Label(
                btn_frame,
                text=desc,
                font=FONTS['tiny'],
                bg=COLORS['bg_card'],
                fg=COLORS['text_muted']
            )
            desc_label.pack()
            
            # Bind click event
            btn_frame.bind('<Button-1>', lambda e, c=code: self.select_piece(c))
            piece_label.bind('<Button-1>', lambda e, c=code: self.select_piece(c))
            name_label.bind('<Button-1>', lambda e, c=code: self.select_piece(c))
            desc_label.bind('<Button-1>', lambda e, c=code: self.select_piece(c))
            
            # Hover effects
            def on_enter(e, frame=btn_frame):
                frame.config(bg=COLORS['bg_secondary'], borderwidth=2)
                for widget in frame.winfo_children():
                    widget.config(bg=COLORS['bg_secondary'])
            
            def on_leave(e, frame=btn_frame):
                frame.config(bg=COLORS['bg_card'], borderwidth=1)
                for widget in frame.winfo_children():
                    widget.config(bg=COLORS['bg_card'])
            
            btn_frame.bind('<Enter>', on_enter)
            btn_frame.bind('<Leave>', on_leave)
    
    def select_piece(self, piece_code):
        """Handle piece selection"""
        self.result = piece_code
        self.destroy()
    
    def show(self):
        """Show dialog and wait for result"""
        self.wait_window()
        return self.result


class GameOverDialog(tk.Toplevel):
    """Beautiful game over dialog"""
    
    def __init__(self, parent, result, reason, my_color):
        """
        Initialize game over dialog
        
        Args:
            parent: Parent window
            result: Game result (white_win/black_win/draw)
            reason: End reason (checkmate/resign/etc)
            my_color: Player's color
        """
        super().__init__(parent)
        
        self.result = result
        self.reason = reason
        self.my_color = my_color
        
        # Window setup
        self.title("Game Over")
        self.resizable(False, False)
        self.configure(bg=COLORS['bg_primary'])
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Center window
        self.update_idletasks()
        width = 450
        height = 350
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create dialog widgets"""
        # Determine outcome
        if self.result == f"{self.my_color}_win":
            outcome = "victory"
            title_text = "🎉 Victory!"
            subtitle_text = "Congratulations! You won the game"
            bg_color = COLORS['success']
            emoji = "🏆"
        elif self.result == "draw":
            outcome = "draw"
            title_text = "🤝 Draw"
            subtitle_text = "The game ended in a draw"
            bg_color = COLORS['info']
            emoji = "🤝"
        else:
            outcome = "defeat"
            title_text = "😞 Defeat"
            subtitle_text = "Better luck next time"
            bg_color = COLORS['danger']
            emoji = "💔"
        
        # Header
        header_frame = tk.Frame(self, bg=bg_color, pady=20)
        header_frame.pack(fill=tk.X)
        
        tk.Label(
            header_frame,
            text=emoji,
            font=('Segoe UI', 60),
            bg=bg_color
        ).pack()
        
        tk.Label(
            header_frame,
            text=title_text,
            font=FONTS['title'],
            bg=bg_color,
            fg=COLORS['text_light']
        ).pack()
        
        tk.Label(
            header_frame,
            text=subtitle_text,
            font=FONTS['body'],
            bg=bg_color,
            fg=COLORS['text_light']
        ).pack(pady=(5, 0))
        
        # Content
        content_frame = tk.Frame(self, bg=COLORS['bg_primary'], padx=30, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Reason
        reason_text = {
            'checkmate': 'Checkmate',
            'resign': 'Resignation',
            'timeout': 'Time Out',
            'stalemate': 'Stalemate',
            'draw_agreement': 'Draw Agreement'
        }.get(self.reason, self.reason)
        
        reason_frame = tk.Frame(content_frame, bg=COLORS['bg_card'], relief='solid', borderwidth=1)
        reason_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            reason_frame,
            text="Game ended by:",
            font=FONTS['small'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_muted']
        ).pack(pady=(10, 5))
        
        tk.Label(
            reason_frame,
            text=reason_text,
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_dark']
        ).pack(pady=(0, 10))
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg=COLORS['bg_primary'])
        button_frame.pack(pady=20)
        
        btn_new = tk.Button(
            button_frame,
            text="New Game",
            command=self.new_game,
            width=15,
            **get_button_style('success', 'normal')
        )
        btn_new.pack(side=tk.LEFT, padx=5, pady=10)
        
        btn_lobby = tk.Button(
            button_frame,
            text="Back to Lobby",
            command=self.back_to_lobby,
            width=15,
            **get_button_style('primary', 'normal')
        )
        btn_lobby.pack(side=tk.LEFT, padx=5, pady=10)
    
    def new_game(self):
        """Start a new game"""
        self.result_action = "new_game"
        self.destroy()
    
    def back_to_lobby(self):
        """Go back to lobby"""
        self.result_action = "lobby"
        self.destroy()
    
    def show(self):
        """Show dialog and wait"""
        self.result_action = "lobby"  # Default
        self.wait_window()
        return self.result_action


class ConfirmDialog(tk.Toplevel):
    """Beautiful confirmation dialog"""
    
    def __init__(self, parent, title, message, style="info"):
        """
        Initialize confirmation dialog
        
        Args:
            parent: Parent window
            title: Dialog title
            message: Message text
            style: Dialog style (info/warning/danger/success)
        """
        super().__init__(parent)
        
        self.result = False
        
        # Window setup
        self.title(title)
        self.resizable(False, False)
        self.configure(bg=COLORS['bg_primary'])
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Center window
        self.update_idletasks()
        width = 380
        height = 220
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        self.create_widgets(title, message, style)
    
    def create_widgets(self, title, message, style):
        """Create dialog widgets"""
        # Style colors
        style_colors = {
            'info': (COLORS['info'], 'ℹ️'),
            'warning': (COLORS['warning'], '⚠️'),
            'danger': (COLORS['danger'], '❌'),
            'success': (COLORS['success'], '✅'),
        }
        
        bg_color, emoji = style_colors.get(style, style_colors['info'])
        
        # Header
        header_frame = tk.Frame(self, bg=bg_color, pady=15)
        header_frame.pack(fill=tk.X)
        
        tk.Label(
            header_frame,
            text=f"{emoji} {title}",
            font=FONTS['heading'],
            bg=bg_color,
            fg=COLORS['text_light']
        ).pack()
        
        # Content
        content_frame = tk.Frame(self, bg=COLORS['bg_primary'], padx=30, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            content_frame,
            text=message,
            font=FONTS['body'],
            bg=COLORS['bg_primary'],
            fg=COLORS['text_dark'],
            wraplength=320,
            justify='center'
        ).pack(pady=20)
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg=COLORS['bg_primary'])
        button_frame.pack()
        
        btn_yes = tk.Button(
            button_frame,
            text="Yes",
            command=self.on_yes,
            width=12,
            **get_button_style('success', 'normal')
        )
        btn_yes.pack(side=tk.LEFT, padx=5, pady=10)
        
        btn_no = tk.Button(
            button_frame,
            text="No",
            command=self.on_no,
            width=12,
            **get_button_style('light', 'normal')
        )
        btn_no.pack(side=tk.LEFT, padx=5, pady=10)
    
    def on_yes(self):
        """Handle Yes button"""
        self.result = True
        self.destroy()
    
    def on_no(self):
        """Handle No button"""
        self.result = False
        self.destroy()
    
    def show(self):
        """Show dialog and wait for result"""
        self.wait_window()
        return self.result
