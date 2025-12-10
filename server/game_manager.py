"""
Game Manager - Handles rooms and game sessions
"""

import uuid
from typing import Dict, Optional, List
from chess_engine import ChessEngine
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.constants import *


class Player:
    """Represents a player in the game"""
    
    def __init__(self, username: str, socket, address):
        self.username = username
        self.socket = socket
        self.address = address
        self.room_id: Optional[str] = None
        self.color: Optional[str] = None
        self.rating = 1200  # Default rating
        
    def __repr__(self):
        return f"Player({self.username})"


class Room:
    """Represents a game room"""
    
    def __init__(self, room_id: str, name: str, creator: Player):
        self.room_id = room_id
        self.name = name
        self.creator = creator
        self.players: List[Player] = [creator]
        self.status = STATUS_WAITING
        self.game: Optional[ChessEngine] = None
        self.white_player: Optional[Player] = None
        self.black_player: Optional[Player] = None
        
    def add_player(self, player: Player) -> bool:
        """Add player to room"""
        if len(self.players) < 2 and player not in self.players:
            self.players.append(player)
            player.room_id = self.room_id
            return True
        return False
    
    def remove_player(self, player: Player):
        """Remove player from room"""
        if player in self.players:
            self.players.remove(player)
            player.room_id = None
            player.color = None
    
    def is_full(self) -> bool:
        """Check if room is full"""
        return len(self.players) >= 2
    
    def start_game(self):
        """Start the chess game"""
        if len(self.players) == 2:
            self.game = ChessEngine()
            self.white_player = self.players[0]
            self.black_player = self.players[1]
            self.white_player.color = COLOR_WHITE
            self.black_player.color = COLOR_BLACK
            self.status = STATUS_PLAYING
            return True
        return False
    
    def get_opponent(self, player: Player) -> Optional[Player]:
        """Get opponent player"""
        if player == self.white_player:
            return self.black_player
        elif player == self.black_player:
            return self.white_player
        return None
    
    def to_dict(self) -> dict:
        """Convert room to dictionary"""
        return {
            "room_id": self.room_id,
            "name": self.name,
            "players": len(self.players),
            "status": self.status,
            "creator": self.creator.username
        }


class GameManager:
    """Manages all game rooms and sessions"""
    
    def __init__(self):
        self.rooms: Dict[str, Room] = {}
        self.players: Dict[str, Player] = {}  # username -> Player
        
    def create_room(self, room_name: str, creator: Player) -> Room:
        """Create a new game room"""
        room_id = str(uuid.uuid4())[:8]
        room = Room(room_id, room_name, creator)
        self.rooms[room_id] = room
        creator.room_id = room_id
        return room
    
    def get_room(self, room_id: str) -> Optional[Room]:
        """Get room by ID"""
        return self.rooms.get(room_id)
    
    def join_room(self, room_id: str, player: Player) -> bool:
        """Join an existing room"""
        room = self.get_room(room_id)
        if room and not room.is_full():
            return room.add_player(player)
        return False
    
    def leave_room(self, player: Player):
        """Leave current room"""
        if player.room_id:
            room = self.get_room(player.room_id)
            if room:
                room.remove_player(player)
                # Remove room if empty
                if len(room.players) == 0:
                    del self.rooms[room.room_id]
    
    def get_available_rooms(self) -> List[dict]:
        """Get list of available rooms"""
        return [
            room.to_dict() 
            for room in self.rooms.values() 
            if room.status == STATUS_WAITING
        ]
    
    def add_player(self, player: Player):
        """Add player to manager"""
        self.players[player.username] = player
    
    def remove_player(self, username: str):
        """Remove player from manager"""
        if username in self.players:
            player = self.players[username]
            self.leave_room(player)
            del self.players[username]
    
    def get_player(self, username: str) -> Optional[Player]:
        """Get player by username"""
        return self.players.get(username)
