"""
Chess Client - Enhanced version with beautiful UI
"""

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, scrolledtext
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.constants import *
from client.network.socket_handler import NetworkHandler
from client.ui.board import ChessBoardUI
from client.ui.styles import COLORS, FONTS, get_button_style
from client.ui.components import ChessTimer, MoveHistory, PlayerInfo, CapturedPieces
from client.ui.dialogs import PawnPromotionDialog, ConfirmDialog, GameOverDialog


class ChessClientEnhanced:
    """Enhanced Chess Client with beautiful UI"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("♟️ Chess Online - Enhanced")
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS['bg_primary'])
        
        self.network = NetworkHandler()
        self.network.set_message_callback(self.handle_message)
        
        # Game state
        self.username = None
        self.opponent_name = None
        self.room_id = None
        self.my_color = None
        self.opponent_color = None
        self.current_turn = None
        self.selected_square = None
        self.legal_moves = []
        self.last_from = None
        self.last_to = None
        
        # UI components
        self.board_ui = None
        self.my_timer = None
        self.opponent_timer = None
        self.move_history = None
        self.my_captured = None
        self.opponent_captured = None
        self.my_player_info = None
        self.opponent_player_info = None
        self.status_label = None
        self.chat_text = None
        self.chat_entry = None
        
        self.setup_login_screen()
    
    def setup_login_screen(self):
        """Setup modern login screen"""
        # Main frame
        main_frame = tk.Frame(self.root, bg=COLORS['bg_primary'], padx=40, pady=30)
        main_frame.pack()
        
        # Title
        title = tk.Label(
            main_frame,
            text="♟️ Chess Online",
            font=FONTS['title'],
            bg=COLORS['bg_primary'],
            fg=COLORS['primary']
        )
        title.pack(pady=(0, 10))
        
        subtitle = tk.Label(
            main_frame,
            text="Play chess with friends online",
            font=FONTS['body'],
            bg=COLORS['bg_primary'],
            fg=COLORS['text_gray']
        )
        subtitle.pack(pady=(0, 30))
        
        # Server IP input
        tk.Label(
            main_frame,
            text="Server IP:",
            font=FONTS['body'],
            bg=COLORS['bg_primary'],
            fg=COLORS['text_dark']
        ).pack(anchor='w')
        
        server_frame = tk.Frame(main_frame, bg=COLORS['bg_primary'])
        server_frame.pack(fill=tk.X, pady=(5, 10))
        
        self.server_entry = tk.Entry(
            server_frame,
            font=FONTS['body'],
            width=25,
            relief=tk.SOLID,
            borderwidth=1
        )
        self.server_entry.insert(0, "127.0.0.1")  # Default localhost
        self.server_entry.pack(side=tk.LEFT, ipady=5)
        
        tk.Label(
            server_frame,
            text="  (localhost hoặc IP bạn)",
            font=FONTS['tiny'],
            bg=COLORS['bg_primary'],
            fg=COLORS['text_muted']
        ).pack(side=tk.LEFT)
        
        # Username input
        tk.Label(
            main_frame,
            text="Username:",
            font=FONTS['body'],
            bg=COLORS['bg_primary'],
            fg=COLORS['text_dark']
        ).pack(anchor='w', pady=(10, 0))
        
        self.username_entry = tk.Entry(
            main_frame,
            font=FONTS['body'],
            width=30,
            relief=tk.SOLID,
            borderwidth=1
        )
        self.username_entry.pack(pady=(5, 20), ipady=5)
        self.username_entry.bind('<Return>', lambda e: self.login())
        self.username_entry.focus()
        
        # Login button
        login_btn = tk.Button(
            main_frame,
            text="Login",
            command=self.login,
            width=20,
            **get_button_style('success'),
            pady=10
        )
        login_btn.pack(pady=5)
        
        # Server info
        server_info = tk.Label(
            main_frame,
            text=f"Server: {SERVER_HOST}:{SERVER_PORT}",
            font=FONTS['small'],
            bg=COLORS['bg_primary'],
            fg=COLORS['text_gray']
        )
        server_info.pack(pady=(20, 0))
    
    def login(self):
        """Handle login"""
        username = self.username_entry.get().strip()
        server_ip = self.server_entry.get().strip()
        
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return
        
        if len(username) < 3:
            messagebox.showerror("Error", "Username must be at least 3 characters")
            return
        
        if not server_ip:
            messagebox.showerror("Error", "Please enter server IP")
            return
        
        # Update network handler with custom IP
        self.network.host = server_ip
        
        # Connect to server
        if not self.network.connect():
            messagebox.showerror("Error", 
                f"Could not connect to server at {server_ip}:5555\n\n"
                "Tips:\n"
                "• Use 127.0.0.1 for localhost\n"
                "• Use friend's IP for LAN (e.g., 192.168.1.100)\n"
                "• Make sure server is running!\n"
                "• Check firewall settings")
            return
        
        # Send login request
        self.network.send(MSG_LOGIN, {"username": username})
    
    def setup_lobby_screen(self):
        """Setup modern lobby screen"""
        # Clear login screen
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.geometry("700x500")
        
        # Main container
        main_frame = tk.Frame(self.root, bg=COLORS['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header = tk.Frame(main_frame, bg=COLORS['bg_primary'])
        header.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            header,
            text=f"Welcome, {self.username}! 👋",
            font=FONTS['heading'],
            bg=COLORS['bg_primary'],
            fg=COLORS['text_dark']
        ).pack(side=tk.LEFT)
        
        # Buttons frame
        btn_frame = tk.Frame(main_frame, bg=COLORS['bg_primary'])
        btn_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Button(
            btn_frame,
            text="➕ Create Room",
            command=self.create_room,
            **get_button_style('success'),
            width=15,
            pady=8
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="🔄 Refresh",
            command=self.refresh_rooms,
            **get_button_style('primary'),
            width=12,
            pady=8
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="🚪 Logout",
            command=self.logout,
            **get_button_style('danger'),
            width=12,
            pady=8
        ).pack(side=tk.RIGHT, padx=5)
        
        # Rooms section
        tk.Label(
            main_frame,
            text="📋 Available Rooms",
            font=FONTS['subheading'],
            bg=COLORS['bg_primary'],
            fg=COLORS['text_dark']
        ).pack(anchor='w', pady=(0, 10))
        
        # Treeview frame
        tree_frame = tk.Frame(main_frame, bg=COLORS['bg_primary'])
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        columns = ('Room Name', 'Owner', 'Players', 'Status')
        self.rooms_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            height=15,
            yscrollcommand=scrollbar.set
        )
        
        # Set column widths
        self.rooms_tree.heading('Room Name', text='Room Name')
        self.rooms_tree.column('Room Name', width=200)
        
        self.rooms_tree.heading('Owner', text='Owner')
        self.rooms_tree.column('Owner', width=120)
        
        self.rooms_tree.heading('Players', text='Players')
        self.rooms_tree.column('Players', width=80)
        
        self.rooms_tree.heading('Status', text='Status')
        self.rooms_tree.column('Status', width=100)
        
        self.rooms_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.rooms_tree.yview)
        
        self.rooms_tree.bind('<Double-Button-1>', self.join_room_from_list)
        
        # Instructions
        tk.Label(
            main_frame,
            text="💡 Double-click a room to join",
            font=FONTS['small'],
            bg=COLORS['bg_primary'],
            fg=COLORS['text_gray']
        ).pack(pady=(10, 0))
        
        # Request room list
        self.refresh_rooms()
    
    def create_room(self):
        """Create a new room"""
        room_name = simpledialog.askstring(
            "Create Room",
            "Enter room name:",
            parent=self.root
        )
        if room_name and room_name.strip():
            self.network.send(MSG_CREATE_ROOM, {"room_name": room_name.strip()})
    
    def refresh_rooms(self):
        """Refresh room list"""
        self.network.send(MSG_LIST_ROOMS, {})
    
    def logout(self):
        """Logout and return to login screen"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.network.send(MSG_LOGOUT, {})
            self.network.disconnect()
            
            # Clear and reset
            for widget in self.root.winfo_children():
                widget.destroy()
            
            self.username = None
            self.root.geometry("")
            self.setup_login_screen()
    
    def join_room_from_list(self, event):
        """Join room from double-click"""
        selection = self.rooms_tree.selection()
        if selection:
            room_id = self.rooms_tree.item(selection[0], 'tags')[0]
            self.network.send(MSG_JOIN_ROOM, {"room_id": room_id})
    
    def setup_game_screen(self):
        """Setup enhanced game screen"""
        # Clear previous screen
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.geometry("1200x700")
        
        # Main container
        main_container = tk.Frame(self.root, bg=COLORS['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left sidebar (Opponent info + Timer)
        left_sidebar = tk.Frame(main_container, bg=COLORS['bg_primary'], width=200)
        left_sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        left_sidebar.pack_propagate(False)
        
        # Opponent info
        opponent_color = COLOR_BLACK if self.my_color == COLOR_WHITE else COLOR_WHITE if self.my_color else None
        self.opponent_player_info = PlayerInfo(
            left_sidebar,
            username=self.opponent_name or "Waiting...",
            color=opponent_color or "white"
        )
        self.opponent_player_info.pack(fill=tk.X, pady=(0, 10))
        
        # Opponent timer
        tk.Label(
            left_sidebar,
            text="⏱ Opponent",
            font=FONTS['small'],
            bg=COLORS['bg_primary'],
            fg=COLORS['text_gray']
        ).pack()
        
        self.opponent_timer = ChessTimer(left_sidebar)
        self.opponent_timer.pack(pady=10)
        
        # Your Losses section (pieces YOU lost to opponent)
        # Your Captures section (pieces you took from opponent)
        tk.Label(
            left_sidebar,
            text="🏆 Your Captures",
            font=FONTS['small_bold'],
            bg=COLORS['bg_primary'],
            fg=COLORS['success']
        ).pack(pady=(15, 5))
        
        tk.Label(
            left_sidebar,
            text="(Pieces you took)",
            font=FONTS['tiny'],
            bg=COLORS['bg_primary'],
            fg=COLORS['text_muted']
        ).pack()
        
        self.my_captured = CapturedPieces(left_sidebar, color="player")
        self.my_captured.pack(pady=5, fill=tk.X)
        
        # Separator
        tk.Frame(left_sidebar, height=2, bg=COLORS['text_muted']).pack(fill=tk.X, pady=15)
        
        # Your Losses section (pieces opponent took from you)
        tk.Label(
            left_sidebar,
            text="💔 Your Losses",
            font=FONTS['small_bold'],
            bg=COLORS['bg_primary'],
            fg=COLORS['danger']
        ).pack(pady=(5, 5))
        
        tk.Label(
            left_sidebar,
            text="(Pieces opponent took)",
            font=FONTS['tiny'],
            bg=COLORS['bg_primary'],
            fg=COLORS['text_muted']
        ).pack()
        
        self.opponent_captured = CapturedPieces(left_sidebar, color="losses")
        self.opponent_captured.pack(pady=5, fill=tk.X)
        
        # Center - Chess board
        center_frame = tk.Frame(main_container, bg=COLORS['bg_primary'])
        center_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Status bar
        self.status_label = tk.Label(
            center_frame,
            text="Waiting for game to start...",
            font=FONTS['body'],
            bg=COLORS['warning'],
            fg=COLORS['text_light'],
            padx=15,
            pady=8,
            relief=tk.SOLID,
            borderwidth=1
        )
        self.status_label.pack(pady=(0, 10))
        
        # Chess board
        flipped = (self.my_color == COLOR_BLACK) if self.my_color else False
        self.board_ui = ChessBoardUI(center_frame, size=560, flipped=flipped)
        self.board_ui.set_click_callback(self.on_square_click)
        
        # My info and timer (bottom of center)
        my_info_frame = tk.Frame(center_frame, bg=COLORS['bg_primary'])
        my_info_frame.pack(pady=(10, 0))
        
        self.my_player_info = PlayerInfo(
            my_info_frame,
            username=self.username,
            color=self.my_color or "white"
        )
        self.my_player_info.pack()
        
        # My timer
        tk.Label(
            center_frame,
            text="⏱ Your Time",
            font=FONTS['small'],
            bg=COLORS['bg_primary'],
            fg=COLORS['text_gray']
        ).pack(pady=(10, 0))
        
        self.my_timer = ChessTimer(center_frame)
        self.my_timer.pack(pady=5)
        
        # My captured pieces (shows pieces I captured from opponent)
        tk.Label(
            center_frame,
            text="🏆 Your Captures",
            font=FONTS['small_bold'],
            bg=COLORS['bg_primary'],
            fg=COLORS['success']
        ).pack(pady=(10, 5))
        
        tk.Label(
            center_frame,
            text="(Pieces you took)",
            font=FONTS['tiny'],
            bg=COLORS['bg_primary'],
            fg=COLORS['text_muted']
        ).pack()
        
        # This shows pieces captured BY me (their pieces lost)
        self.my_captured = CapturedPieces(center_frame, color="player")
        self.my_captured.pack(pady=5)
        
        # Right sidebar (Move history + Chat + Controls)
        right_sidebar = tk.Frame(main_container, bg=COLORS['bg_primary'], width=300)
        right_sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        right_sidebar.pack_propagate(False)
        
        # Move history
        self.move_history = MoveHistory(right_sidebar)
        self.move_history.pack(fill=tk.BOTH, expand=False, pady=(0, 15))
        
        # Chat section
        tk.Label(
            right_sidebar,
            text="💬 Chat",
            font=FONTS['subheading'],
            bg=COLORS['bg_primary'],
            fg=COLORS['text_dark']
        ).pack(anchor='w')
        
        # Chat display
        chat_frame = tk.Frame(right_sidebar)
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.chat_text = scrolledtext.ScrolledText(
            chat_frame,
            height=8,
            width=35,
            font=FONTS['small'],
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_dark'],
            relief=tk.SOLID,
            borderwidth=1,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.chat_text.pack(fill=tk.BOTH, expand=True)
        
        # Chat input
        chat_input_frame = tk.Frame(right_sidebar, bg=COLORS['bg_primary'])
        chat_input_frame.pack(fill=tk.X, pady=(5, 15))
        
        self.chat_entry = tk.Entry(
            chat_input_frame,
            font=FONTS['small'],
            relief=tk.SOLID,
            borderwidth=1
        )
        self.chat_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.chat_entry.bind('<Return>', lambda e: self.send_chat())
        
        tk.Button(
            chat_input_frame,
            text="Send",
            command=self.send_chat,
            **get_button_style('primary'),
            width=8
        ).pack(side=tk.RIGHT)
        
        # Control buttons
        tk.Label(
            right_sidebar,
            text="🎮 Game Controls",
            font=FONTS['subheading'],
            bg=COLORS['bg_primary'],
            fg=COLORS['text_dark']
        ).pack(anchor='w', pady=(0, 10))
        
        control_frame = tk.Frame(right_sidebar, bg=COLORS['bg_primary'])
        control_frame.pack(fill=tk.X)
        
        # Undo/Redo buttons in a row
        undo_redo_frame = tk.Frame(control_frame, bg=COLORS['bg_primary'])
        undo_redo_frame.pack(fill=tk.X, pady=3)
        
        self.undo_btn = tk.Button(
            undo_redo_frame,
            text="↶ Undo",
            command=self.undo_move,
            **get_button_style('secondary'),
            width=6,
            state=tk.DISABLED
        )
        self.undo_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))
        
        self.redo_btn = tk.Button(
            undo_redo_frame,
            text="↷ Redo",
            command=self.redo_move,
            **get_button_style('secondary'),
            width=6,
            state=tk.DISABLED
        )
        self.redo_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))
        
        tk.Button(
            control_frame,
            text="🏳 Resign",
            command=self.resign,
            **get_button_style('danger'),
            width=12
        ).pack(fill=tk.X, pady=3)
        
        tk.Button(
            control_frame,
            text="🤝 Offer Draw",
            command=self.offer_draw,
            **get_button_style('warning'),
            width=12
        ).pack(fill=tk.X, pady=3)
        
        tk.Button(
            control_frame,
            text="🔄 Request Rematch",
            command=self.request_rematch,
            **get_button_style('success'),
            width=12
        ).pack(fill=tk.X, pady=3)
        
        tk.Button(
            control_frame,
            text="⛶ Toggle Fullscreen",
            command=self.toggle_fullscreen,
            **get_button_style('dark'),
            width=12
        ).pack(fill=tk.X, pady=3)
        
        tk.Button(
            control_frame,
            text="🚪 Leave Game",
            command=self.leave_game,
            **get_button_style('dark'),
            width=12
        ).pack(fill=tk.X, pady=3)
    
    def on_square_click(self, row: int, col: int):
        """Handle square click on chess board"""
        if not self.board_ui or not self.my_color:
            return
        
        # Check if it's our turn
        if self.current_turn != self.my_color:
            self.add_chat_message("System", "⚠️ It's not your turn!", is_system=True)
            return
        
        square = self.board_ui.coords_to_square(row, col)
        
        if self.selected_square is None:
            # Select piece - request legal moves
            piece = self.board_ui.pieces.get((row, col))
            if piece:
                self.selected_square = square
                self.board_ui.select_square(row, col)
                # Request legal moves from server
                self.network.send("GET_LEGAL_MOVES", {"square": square})
        else:
            # Make move
            from_square = self.selected_square
            to_square = square
            
            # Check if this is a pawn promotion
            promotion = None
            from_row, from_col = self.board_ui.square_to_coords(from_square)
            to_row, to_col = self.board_ui.square_to_coords(to_square)
            
            piece = self.board_ui.pieces.get((from_row, from_col))
            if piece and piece.lower() == 'p':
                # White pawn reaches row 0, black pawn reaches row 7
                if (self.my_color == 'white' and to_row == 0) or \
                   (self.my_color == 'black' and to_row == 7):
                    # Show promotion dialog
                    dialog = PawnPromotionDialog(self.root, self.my_color)
                    promotion = dialog.show()
                    if not promotion:
                        # User closed dialog without selecting, default to Queen
                        promotion = 'Q' if self.my_color == 'white' else 'q'
            
            # Send move to server
            self.network.send(MSG_MOVE, {
                "from": from_square,
                "to": to_square,
                "promotion": promotion
            })
            
            # Clear selection
            self.selected_square = None
            self.legal_moves = []
            self.board_ui.clear_selection()
    
    def send_chat(self):
        """Send chat message"""
        message = self.chat_entry.get().strip()
        if message:
            self.network.send(MSG_CHAT, {"message": message})
            self.chat_entry.delete(0, tk.END)
    
    def add_chat_message(self, username: str, message: str, is_system=False):
        """Add message to chat"""
        if self.chat_text:
            self.chat_text.config(state=tk.NORMAL)
            
            if is_system:
                self.chat_text.insert(tk.END, f"🔔 {message}\n", 'system')
                self.chat_text.tag_config('system', foreground=COLORS['warning'])
            else:
                prefix = "You" if username == self.username else username
                self.chat_text.insert(tk.END, f"{prefix}: {message}\n")
            
            self.chat_text.see(tk.END)
            self.chat_text.config(state=tk.DISABLED)
    
    def resign(self):
        """Resign from game"""
        dialog = ConfirmDialog(
            self.root,
            "Resign Game",
            "Are you sure you want to resign?\nYou will lose the game.",
            "warning"
        )
        if dialog.show():
            self.network.send(MSG_RESIGN, {})
    
    def offer_draw(self):
        """Offer draw to opponent"""
        self.network.send(MSG_OFFER_DRAW, {})
        self.add_chat_message("System", "Draw offer sent to opponent", is_system=True)
    
    def request_rematch(self):
        """Request a rematch after game over"""
        self.add_chat_message("System", "Rematch feature coming soon!", is_system=True)
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        current_state = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current_state)
        if not current_state:
            self.add_chat_message("System", "Press ESC to exit fullscreen", is_system=True)
    
    def leave_game(self):
        """Leave current game"""
        if messagebox.askyesno("Leave Game", "Are you sure you want to leave?"):
            self.network.send(MSG_LEAVE_ROOM, {})
            self.setup_lobby_screen()
    
    def undo_move(self):
        """Request undo last move"""
        if self.network:
            self.network.send(MSG_UNDO, {})
    
    def redo_move(self):
        """Request redo last undone move"""
        if self.network:
            self.network.send(MSG_REDO, {})
    
    def handle_message(self, message: dict):
        """Handle incoming message from server"""
        msg_type = message.get("type")
        data = message.get("data", {})
        
        # Schedule UI updates in main thread
        self.root.after(0, lambda: self._process_message(msg_type, data))
    
    def _process_message(self, msg_type: str, data: dict):
        """Process message in main thread"""
        if msg_type == MSG_LOGIN_SUCCESS:
            self.username = data.get("username")
            self.setup_lobby_screen()
        
        elif msg_type == MSG_LOGIN_FAILED:
            messagebox.showerror("Login Failed", data.get("error"))
            self.network.disconnect()
        
        elif msg_type == MSG_ROOM_LIST:
            self.update_room_list(data.get("rooms", []))
        
        elif msg_type == MSG_ROOM_JOINED:
            self.room_id = data.get("room_id")
            self.my_color = data.get("your_color")
            if not self.my_color:
                # Waiting for opponent
                self.setup_game_screen()
        
        elif msg_type == MSG_GAME_START:
            self.room_id = data.get("game_id")
            self.my_color = data.get("your_color")
            self.opponent_name = data.get("black_player") if self.my_color == COLOR_WHITE else data.get("white_player")
            self.setup_game_screen()
            self.update_board(data.get("board_state"))
            self.current_turn = COLOR_WHITE
            self.update_turn_display()
            self.status_label.config(
                text="🎮 Game Started! White to move",
                bg=COLORS['success'],
                fg=COLORS['text_light']
            )
            # Start timers
            if self.my_color == COLOR_WHITE:
                self.my_timer.start()
            else:
                self.opponent_timer.start()
        
        elif msg_type == "LEGAL_MOVES":
            square = data.get("square")
            moves = data.get("moves", [])
            if moves:
                # Highlight legal moves
                coords = [self.board_ui.square_to_coords(m) for m in moves]
                self.board_ui.highlight_squares(coords)
        
        elif msg_type == MSG_MOVE_UPDATE:
            from_sq = data.get("from")
            to_sq = data.get("to")
            captured_piece = data.get("captured_piece")
            
            self.update_board(data.get("board_state"))
            self.current_turn = data.get("current_turn")
            
            # Update last move highlight
            if from_sq and to_sq:
                self.board_ui.set_last_move(from_sq, to_sq)
            
            # Update captured pieces display
            # captured_by_white = pieces white captured (black pieces lost)
            # captured_by_black = pieces black captured (white pieces lost)
            if self.my_captured and self.opponent_captured:
                captured_by_white = data.get("captured_by_white", [])  # Black pieces white captured
                captured_by_black = data.get("captured_by_black", [])  # White pieces black captured
                
                if self.my_color == COLOR_WHITE:
                    # I am WHITE:
                    # - "Your Captures" shows BLACK pieces I captured → captured_by_white
                    # - "Your Losses" shows WHITE pieces opponent captured → captured_by_black
                    self.my_captured.set_pieces(captured_by_white)      # Black pieces
                    self.opponent_captured.set_pieces(captured_by_black)  # White pieces
                else:
                    # I am BLACK:
                    # - "Your Captures" shows WHITE pieces I captured → captured_by_black
                    # - "Your Losses" shows BLACK pieces opponent captured → captured_by_white
                    self.my_captured.set_pieces(captured_by_black)      # White pieces
                    self.opponent_captured.set_pieces(captured_by_white)  # Black pieces
            
            # Add to move history
            if self.move_history and from_sq and to_sq:
                # Simple notation (could be improved)
                move_color = COLOR_WHITE if self.current_turn == COLOR_BLACK else COLOR_WHITE
                capture_symbol = "x" if captured_piece else "-"
                self.move_history.add_move(f"{from_sq}{capture_symbol}{to_sq}", move_color)
            
            # Update undo/redo button states
            can_undo = data.get("can_undo", False)
            can_redo = data.get("can_redo", False)
            
            if hasattr(self, 'undo_btn'):
                self.undo_btn.config(state=tk.NORMAL if can_undo else tk.DISABLED)
            if hasattr(self, 'redo_btn'):
                self.redo_btn.config(state=tk.NORMAL if can_redo else tk.DISABLED)
            
            self.update_turn_display()
            
            # Switch timers
            if self.current_turn == self.my_color:
                self.my_timer.start()
                self.opponent_timer.pause()
            else:
                self.opponent_timer.start()
                self.my_timer.pause()
        
        elif msg_type == MSG_GAME_OVER:
            result = data.get("result")
            reason = data.get("reason")
            self.show_game_over(result, reason)
            # Stop timers
            if self.my_timer:
                self.my_timer.pause()
            if self.opponent_timer:
                self.opponent_timer.pause()
        
        elif msg_type == MSG_CHAT_MESSAGE:
            username = data.get("username")
            message = data.get("message")
            self.add_chat_message(username, message)
        
        elif msg_type == MSG_ERROR:
            error = data.get("error")
            self.add_chat_message("Error", error, is_system=True)
    
    def update_room_list(self, rooms: list):
        """Update room list in lobby"""
        if hasattr(self, 'rooms_tree'):
            # Clear existing items
            for item in self.rooms_tree.get_children():
                self.rooms_tree.delete(item)
            
            # Add rooms
            for room in rooms:
                self.rooms_tree.insert('', tk.END, values=(
                    room['name'],
                    room.get('creator', 'Unknown'),
                    f"{room['players']}/2",
                    room['status'].capitalize()
                ), tags=(room['room_id'],))
    
    def update_board(self, fen: str):
        """Update board display"""
        if self.board_ui:
            self.board_ui.set_position(fen)
    
    def update_turn_display(self):
        """Update turn indicator"""
        if self.my_player_info and self.opponent_player_info and self.my_color:
            if self.current_turn == self.my_color:
                self.my_player_info.set_active(True)
                self.opponent_player_info.set_active(False)
                self.status_label.config(
                    text="🟢 YOUR TURN - Make your move!",
                    bg=COLORS['success'],
                    fg=COLORS['text_light']
                )
            else:
                self.my_player_info.set_active(False)
                self.opponent_player_info.set_active(True)
                self.status_label.config(
                    text="⏳ Opponent's Turn - Please wait",
                    bg=COLORS['warning'],
                    fg=COLORS['text_light']
                )
    
    def show_game_over(self, result: str, reason: str):
        """Show game over dialog"""
        reason_text = {
            END_CHECKMATE: "checkmate",
            END_RESIGN: "resign",
            END_TIMEOUT: "timeout",
            END_STALEMATE: "stalemate",
            END_DRAW: "draw_agreement"
        }.get(reason, reason)
        
        # Update status bar
        status_texts = {
            "checkmate": "Checkmate",
            "resign": "Resignation",
            "timeout": "Time Out",
            "stalemate": "Stalemate",
            "draw_agreement": "Draw Agreement"
        }
        
        self.status_label.config(
            text=f"Game Over - {status_texts.get(reason_text, reason_text)}",
            bg=COLORS['danger'],
            fg=COLORS['text_light']
        )
        
        # Show beautiful game over dialog
        dialog = GameOverDialog(self.root, result, reason_text, self.my_color)
        action = dialog.show()
        
        if action == "new_game":
            # Go back to lobby to start a new game
            self.setup_lobby_screen()
        else:
            # Go back to lobby
            self.setup_lobby_screen()
    
    def run(self):
        """Run the client application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Bind ESC key to exit fullscreen
        self.root.bind('<Escape>', lambda e: self.root.attributes('-fullscreen', False))
        
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')
        
        self.root.mainloop()
    
    def on_close(self):
        """Handle window close"""
        if self.network.connected:
            self.network.send(MSG_LOGOUT, {})
            self.network.disconnect()
        self.root.destroy()


def main():
    """Main entry point"""
    client = ChessClientEnhanced()
    client.run()


if __name__ == "__main__":
    main()
