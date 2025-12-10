"""
Chess Client - Main client application
"""

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.constants import *
from client.network.socket_handler import NetworkHandler
from client.ui.board import ChessBoardUI


class ChessClient:
    """Main Chess Client application"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("♟️ Chess Online")
        self.root.resizable(False, False)
        
        self.network = NetworkHandler()
        self.network.set_message_callback(self.handle_message)
        
        self.username = None
        self.room_id = None
        self.my_color = None
        self.current_turn = None
        self.selected_square = None
        
        self.board_ui = None
        self.status_label = None
        self.chat_text = None
        self.chat_entry = None
        self.turn_label = None
        
        self.setup_login_screen()
    
    def setup_login_screen(self):
        """Setup login screen"""
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack()
        
        tk.Label(frame, text="♟️ Chess Online", font=('Arial', 24, 'bold')).pack(pady=10)
        tk.Label(frame, text="Enter your username:", font=('Arial', 12)).pack(pady=5)
        
        self.username_entry = tk.Entry(frame, font=('Arial', 14), width=20)
        self.username_entry.pack(pady=5)
        self.username_entry.bind('<Return>', lambda e: self.login())
        
        tk.Button(
            frame, 
            text="Login", 
            font=('Arial', 12),
            command=self.login,
            bg='#4CAF50',
            fg='white',
            padx=20,
            pady=5
        ).pack(pady=10)
        
        self.username_entry.focus()
    
    def login(self):
        """Handle login"""
        username = self.username_entry.get().strip()
        
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return
        
        # Connect to server
        if not self.network.connect():
            messagebox.showerror("Error", "Could not connect to server")
            return
        
        # Send login request
        self.network.send(MSG_LOGIN, {"username": username})
    
    def setup_lobby_screen(self):
        """Setup lobby/room selection screen"""
        # Clear login screen
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.geometry("600x400")
        
        # Title
        tk.Label(
            self.root, 
            text=f"Welcome, {self.username}!", 
            font=('Arial', 18, 'bold')
        ).pack(pady=10)
        
        # Buttons frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="Create Room",
            font=('Arial', 12),
            command=self.create_room,
            bg='#2196F3',
            fg='white',
            padx=20,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Refresh Rooms",
            font=('Arial', 12),
            command=self.refresh_rooms,
            bg='#FF9800',
            fg='white',
            padx=20,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        # Rooms list
        tk.Label(self.root, text="Available Rooms:", font=('Arial', 14)).pack(pady=5)
        
        # Create treeview for rooms
        columns = ('Room Name', 'Players', 'Status')
        self.rooms_tree = ttk.Treeview(self.root, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.rooms_tree.heading(col, text=col)
            self.rooms_tree.column(col, width=180)
        
        self.rooms_tree.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        self.rooms_tree.bind('<Double-Button-1>', self.join_room_from_list)
        
        # Request room list
        self.refresh_rooms()
    
    def create_room(self):
        """Create a new room"""
        room_name = simpledialog.askstring("Create Room", "Enter room name:")
        if room_name:
            self.network.send(MSG_CREATE_ROOM, {"room_name": room_name})
    
    def refresh_rooms(self):
        """Refresh room list"""
        self.network.send(MSG_LIST_ROOMS, {})
    
    def join_room_from_list(self, event):
        """Join room from double-click"""
        selection = self.rooms_tree.selection()
        if selection:
            item = self.rooms_tree.item(selection[0])
            # Get room_id from item (we'll store it as a tag)
            room_id = self.rooms_tree.item(selection[0], 'tags')[0]
            self.network.send(MSG_JOIN_ROOM, {"room_id": room_id})
    
    def setup_game_screen(self):
        """Setup game screen"""
        # Clear lobby screen
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.geometry("800x600")
        
        # Main container
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left side - Chess board
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Status
        self.status_label = tk.Label(
            left_frame,
            text="Waiting for opponent...",
            font=('Arial', 12),
            bg='#FFC107',
            fg='black',
            padx=10,
            pady=5
        )
        self.status_label.pack(pady=5)
        
        # Turn indicator
        self.turn_label = tk.Label(
            left_frame,
            text="",
            font=('Arial', 14, 'bold')
        )
        self.turn_label.pack(pady=5)
        
        # Chess board
        flipped = (self.my_color == COLOR_BLACK)
        self.board_ui = ChessBoardUI(left_frame, size=512, flipped=flipped)
        self.board_ui.set_click_callback(self.on_square_click)
        
        # Right side - Chat and controls
        right_frame = tk.Frame(main_frame, width=250)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Chat
        tk.Label(right_frame, text="Chat", font=('Arial', 14, 'bold')).pack()
        
        self.chat_text = tk.Text(right_frame, height=20, width=30, state=tk.DISABLED)
        self.chat_text.pack(pady=5)
        
        # Chat entry
        chat_input_frame = tk.Frame(right_frame)
        chat_input_frame.pack(fill=tk.X)
        
        self.chat_entry = tk.Entry(chat_input_frame, font=('Arial', 10))
        self.chat_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.chat_entry.bind('<Return>', lambda e: self.send_chat())
        
        tk.Button(
            chat_input_frame,
            text="Send",
            command=self.send_chat
        ).pack(side=tk.RIGHT)
        
        # Control buttons
        control_frame = tk.Frame(right_frame)
        control_frame.pack(pady=10)
        
        tk.Button(
            control_frame,
            text="Resign",
            command=self.resign,
            bg='#F44336',
            fg='white',
            padx=10
        ).pack(pady=5, fill=tk.X)
        
        tk.Button(
            control_frame,
            text="Offer Draw",
            command=self.offer_draw,
            bg='#9E9E9E',
            fg='white',
            padx=10
        ).pack(pady=5, fill=tk.X)
    
    def on_square_click(self, row: int, col: int):
        """Handle square click on chess board"""
        if not self.board_ui or not self.my_color:
            return
        
        # Check if it's our turn
        if self.current_turn != self.my_color:
            self.add_chat_message("System", "It's not your turn!")
            return
        
        square = self.board_ui.coords_to_square(row, col)
        
        if self.selected_square is None:
            # Select piece
            self.selected_square = square
            self.board_ui.select_square(row, col)
        else:
            # Make move
            from_square = self.selected_square
            to_square = square
            
            # Send move to server
            self.network.send(MSG_MOVE, {
                "from": from_square,
                "to": to_square,
                "promotion": None  # TODO: Handle promotion
            })
            
            # Clear selection
            self.selected_square = None
            self.board_ui.clear_selection()
    
    def send_chat(self):
        """Send chat message"""
        message = self.chat_entry.get().strip()
        if message:
            self.network.send(MSG_CHAT, {"message": message})
            self.chat_entry.delete(0, tk.END)
    
    def add_chat_message(self, username: str, message: str):
        """Add message to chat"""
        if self.chat_text:
            self.chat_text.config(state=tk.NORMAL)
            self.chat_text.insert(tk.END, f"{username}: {message}\n")
            self.chat_text.see(tk.END)
            self.chat_text.config(state=tk.DISABLED)
    
    def resign(self):
        """Resign from game"""
        if messagebox.askyesno("Resign", "Are you sure you want to resign?"):
            self.network.send(MSG_RESIGN, {})
    
    def offer_draw(self):
        """Offer draw to opponent"""
        self.network.send(MSG_OFFER_DRAW, {})
        self.add_chat_message("System", "Draw offer sent")
    
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
            self.setup_game_screen()
            self.update_board(data.get("board_state"))
            self.current_turn = COLOR_WHITE
            self.update_turn_display()
            self.status_label.config(text="Game Started!", bg='#4CAF50')
        
        elif msg_type == MSG_MOVE_UPDATE:
            self.update_board(data.get("board_state"))
            self.current_turn = data.get("current_turn")
            self.update_turn_display()
        
        elif msg_type == MSG_GAME_OVER:
            result = data.get("result")
            reason = data.get("reason")
            self.show_game_over(result, reason)
        
        elif msg_type == MSG_CHAT_MESSAGE:
            username = data.get("username")
            message = data.get("message")
            self.add_chat_message(username, message)
        
        elif msg_type == MSG_ERROR:
            error = data.get("error")
            self.add_chat_message("Error", error)
    
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
                    f"{room['players']}/2",
                    room['status']
                ), tags=(room['room_id'],))
    
    def update_board(self, fen: str):
        """Update board display"""
        if self.board_ui:
            self.board_ui.set_position(fen)
    
    def update_turn_display(self):
        """Update turn indicator"""
        if self.turn_label and self.my_color:
            if self.current_turn == self.my_color:
                self.turn_label.config(
                    text="YOUR TURN",
                    fg='green'
                )
            else:
                self.turn_label.config(
                    text="Opponent's Turn",
                    fg='red'
                )
    
    def show_game_over(self, result: str, reason: str):
        """Show game over dialog"""
        if result == f"{self.my_color}_win":
            message = f"You Won! ({reason})"
        elif result == "draw":
            message = f"Draw ({reason})"
        else:
            message = f"You Lost ({reason})"
        
        self.status_label.config(text=message, bg='#FF5722')
        messagebox.showinfo("Game Over", message)
    
    def run(self):
        """Run the client application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()
    
    def on_close(self):
        """Handle window close"""
        if self.network.connected:
            self.network.send(MSG_LOGOUT, {})
            self.network.disconnect()
        self.root.destroy()


def main():
    """Main entry point"""
    client = ChessClient()
    client.run()


if __name__ == "__main__":
    main()
