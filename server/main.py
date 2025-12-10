"""
Chess Server - Main server application
Handles socket connections and client requests
"""

import socket
import threading
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.constants import *
from common.protocol import create_message, parse_message, send_message, receive_message
from game_manager import GameManager, Player


class ChessServer:
    """Main Chess Server class"""
    
    def __init__(self, host=SERVER_HOST, port=SERVER_PORT):
        self.host = host
        self.port = port
        self.server_socket = None
        self.game_manager = GameManager()
        self.running = False
        
    def start(self):
        """Start the chess server"""
        try:
            # Create server socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(MAX_CONNECTIONS)
            
            self.running = True
            print(f"♟️  Chess Server started on {self.host}:{self.port}")
            print(f"📡 Waiting for connections...")
            
            # Accept connections
            while self.running:
                try:
                    client_socket, address = self.server_socket.accept()
                    print(f"✅ New connection from {address}")
                    
                    # Create thread for client
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, address),
                        daemon=True
                    )
                    client_thread.start()
                    
                except Exception as e:
                    if self.running:
                        print(f"❌ Error accepting connection: {e}")
                        
        except Exception as e:
            print(f"❌ Server error: {e}")
        finally:
            self.shutdown()
    
    def handle_client(self, client_socket, address):
        """Handle individual client connection"""
        player = None
        
        try:
            while self.running:
                # Receive message from client
                message = receive_message(client_socket, BUFFER_SIZE)
                
                if not message:
                    break
                
                msg_type = message.get("type")
                data = message.get("data", {})
                
                print(f"📨 Received {msg_type} from {address}")
                
                # Handle different message types
                if msg_type == MSG_LOGIN:
                    player = self.handle_login(client_socket, data, address)
                    
                elif msg_type == MSG_CREATE_ROOM:
                    self.handle_create_room(client_socket, player, data)
                    
                elif msg_type == MSG_LIST_ROOMS:
                    self.handle_list_rooms(client_socket)
                    
                elif msg_type == MSG_JOIN_ROOM:
                    self.handle_join_room(client_socket, player, data)
                    
                elif msg_type == MSG_MOVE:
                    self.handle_move(client_socket, player, data)
                
                elif msg_type == "GET_LEGAL_MOVES":
                    self.handle_get_legal_moves(client_socket, player, data)
                    
                elif msg_type == MSG_CHAT:
                    self.handle_chat(player, data)
                    
                elif msg_type == MSG_RESIGN:
                    self.handle_resign(player)
                    
                elif msg_type == MSG_LOGOUT:
                    break
                    
        except Exception as e:
            print(f"❌ Error handling client {address}: {e}")
        finally:
            # Cleanup
            if player:
                print(f"👋 {player.username} disconnected")
                self.game_manager.remove_player(player.username)
            client_socket.close()
    
    def handle_login(self, client_socket, data, address):
        """Handle login request"""
        username = data.get("username", "")
        
        if not username:
            send_message(client_socket, MSG_LOGIN_FAILED, 
                        {"error": "Username required"})
            return None
        
        # Check if username already exists
        if self.game_manager.get_player(username):
            send_message(client_socket, MSG_LOGIN_FAILED,
                        {"error": "Username already taken"})
            return None
        
        # Create player
        player = Player(username, client_socket, address)
        self.game_manager.add_player(player)
        
        # Send success
        send_message(client_socket, MSG_LOGIN_SUCCESS, {
            "username": username,
            "rating": player.rating
        })
        
        print(f"✅ {username} logged in")
        return player
    
    def handle_create_room(self, client_socket, player, data):
        """Handle create room request"""
        if not player:
            send_message(client_socket, MSG_ERROR, {"error": "Not logged in"})
            return
        
        room_name = data.get("room_name", f"{player.username}'s room")
        room = self.game_manager.create_room(room_name, player)
        
        send_message(client_socket, MSG_ROOM_JOINED, {
            "room_id": room.room_id,
            "room_name": room.name,
            "status": room.status
        })
        
        print(f"🏠 {player.username} created room {room.room_id}")
    
    def handle_list_rooms(self, client_socket):
        """Handle list rooms request"""
        rooms = self.game_manager.get_available_rooms()
        send_message(client_socket, MSG_ROOM_LIST, {"rooms": rooms})
    
    def handle_join_room(self, client_socket, player, data):
        """Handle join room request"""
        if not player:
            send_message(client_socket, MSG_ERROR, {"error": "Not logged in"})
            return
        
        room_id = data.get("room_id")
        room = self.game_manager.get_room(room_id)
        
        if not room:
            send_message(client_socket, MSG_ERROR, {"error": "Room not found"})
            return
        
        if room.is_full():
            send_message(client_socket, MSG_ERROR, {"error": "Room is full"})
            return
        
        # Join room
        if self.game_manager.join_room(room_id, player):
            send_message(client_socket, MSG_ROOM_JOINED, {
                "room_id": room.room_id,
                "room_name": room.name
            })
            
            # Start game if room is full
            if room.is_full():
                room.start_game()
                self.broadcast_game_start(room)
            
            print(f"🚪 {player.username} joined room {room.room_id}")
    
    def broadcast_game_start(self, room):
        """Broadcast game start to both players"""
        game_data = {
            "game_id": room.room_id,
            "white_player": room.white_player.username,
            "black_player": room.black_player.username,
            "board_state": room.game.get_board_state()
        }
        
        # Send to white player
        send_message(room.white_player.socket, MSG_GAME_START, {
            **game_data,
            "your_color": COLOR_WHITE
        })
        
        # Send to black player
        send_message(room.black_player.socket, MSG_GAME_START, {
            **game_data,
            "your_color": COLOR_BLACK
        })
        
        print(f"🎮 Game started in room {room.room_id}")
    
    def handle_get_legal_moves(self, client_socket, player, data):
        """Handle get legal moves request"""
        if not player or not player.room_id:
            send_message(client_socket, MSG_ERROR, {"error": "Not in a game"})
            return
        
        room = self.game_manager.get_room(player.room_id)
        if not room or not room.game:
            send_message(client_socket, MSG_ERROR, {"error": "Game not found"})
            return
        
        square = data.get("square")
        if square:
            # Check if piece belongs to current player
            piece_color = room.game.get_piece_color(square)
            if piece_color == player.color:
                legal_moves = room.game.get_legal_moves(square)
                send_message(client_socket, "LEGAL_MOVES", {
                    "square": square,
                    "moves": legal_moves
                })
            else:
                send_message(client_socket, "LEGAL_MOVES", {
                    "square": square,
                    "moves": []
                })
    
    def handle_move(self, client_socket, player, data):
        """Handle move request"""
        if not player or not player.room_id:
            send_message(client_socket, MSG_ERROR, {"error": "Not in a game"})
            return
        
        room = self.game_manager.get_room(player.room_id)
        if not room or not room.game:
            send_message(client_socket, MSG_ERROR, {"error": "Game not found"})
            return
        
        # Check if it's player's turn
        current_turn = room.game.get_current_turn()
        if player.color != current_turn:
            send_message(client_socket, MSG_ERROR, {"error": "Not your turn"})
            return
        
        # Make move
        from_square = data.get("from")
        to_square = data.get("to")
        promotion = data.get("promotion")
        
        move_result = room.game.make_move(from_square, to_square, promotion)
        if move_result[0]:  # Move was successful
            captured_piece = move_result[1] if len(move_result) > 1 else None
            
            # Broadcast move to both players
            move_data = {
                "from": from_square,
                "to": to_square,
                "promotion": promotion,
                "board_state": room.game.get_board_state(),
                "current_turn": room.game.get_current_turn(),
                "captured_piece": captured_piece,
                "captured_by_white": room.game.captured_by_white,
                "captured_by_black": room.game.captured_by_black
            }
            
            send_message(room.white_player.socket, MSG_MOVE_UPDATE, move_data)
            send_message(room.black_player.socket, MSG_MOVE_UPDATE, move_data)
            
            # Check game over
            if room.game.is_game_over():
                result = room.game.get_game_result()
                self.broadcast_game_over(room, result)
        else:
            # Send more detailed error
            send_message(client_socket, MSG_ERROR, {"error": "Invalid move"})
    
    def handle_chat(self, player, data):
        """Handle chat message"""
        if not player or not player.room_id:
            return
        
        room = self.game_manager.get_room(player.room_id)
        if not room:
            return
        
        message = data.get("message", "")
        chat_data = {
            "username": player.username,
            "message": message
        }
        
        # Broadcast to both players
        for p in room.players:
            send_message(p.socket, MSG_CHAT_MESSAGE, chat_data)
    
    def handle_resign(self, player):
        """Handle resign request"""
        if not player or not player.room_id:
            return
        
        room = self.game_manager.get_room(player.room_id)
        if not room:
            return
        
        # Determine winner
        winner = COLOR_BLACK if player.color == COLOR_WHITE else COLOR_WHITE
        self.broadcast_game_over(room, f"{winner}_win", END_RESIGN)
    
    def broadcast_game_over(self, room, result, reason=END_CHECKMATE):
        """Broadcast game over to both players"""
        game_over_data = {
            "result": result,
            "reason": reason
        }
        
        for player in room.players:
            send_message(player.socket, MSG_GAME_OVER, game_over_data)
        
        room.status = STATUS_FINISHED
        print(f"🏁 Game over in room {room.room_id}: {result}")
    
    def shutdown(self):
        """Shutdown server"""
        print("\n🛑 Shutting down server...")
        self.running = False
        if self.server_socket:
            self.server_socket.close()


def main():
    """Main entry point"""
    server = ChessServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
        server.shutdown()


if __name__ == "__main__":
    main()
