"""
Save and load game functionality
Saves games in PGN format
"""

import chess.pgn
import os
import json
from datetime import datetime
from typing import Optional, Dict, List
import io


class GameSaver:
    """Handles saving and loading chess games"""
    
    def __init__(self, save_dir: str = None):
        if save_dir is None:
            save_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'saved_games')
        
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)
    
    def save_game(self, board: chess.Board, white_player: str, black_player: str,
                  result: str, metadata: Optional[Dict] = None) -> str:
        """
        Save a game in PGN format
        
        Args:
            board: Chess board with game history
            white_player: White player name
            black_player: Black player name
            result: Game result ('1-0', '0-1', '1/2-1/2', or '*')
            metadata: Additional game metadata
            
        Returns:
            Path to saved file
        """
        # Create PGN game
        game = chess.pgn.Game()
        
        # Set headers
        game.headers["Event"] = "Chess Online Game"
        game.headers["Site"] = "Chess Online"
        game.headers["Date"] = datetime.now().strftime("%Y.%m.%d")
        game.headers["Round"] = "1"
        game.headers["White"] = white_player
        game.headers["Black"] = black_player
        game.headers["Result"] = result
        
        # Add metadata
        if metadata:
            for key, value in metadata.items():
                game.headers[key] = str(value)
        
        # Add moves
        node = game
        for move in board.move_stack:
            node = node.add_variation(move)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{white_player}_vs_{black_player}_{timestamp}.pgn"
        filepath = os.path.join(self.save_dir, filename)
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            exporter = chess.pgn.FileExporter(f)
            game.accept(exporter)
        
        return filepath
    
    def load_game(self, filepath: str) -> Optional[chess.pgn.Game]:
        """
        Load a game from PGN file
        
        Args:
            filepath: Path to PGN file
            
        Returns:
            Loaded chess game
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                game = chess.pgn.read_game(f)
            return game
        except Exception as e:
            print(f"Error loading game: {e}")
            return None
    
    def list_saved_games(self) -> List[Dict]:
        """
        Get list of all saved games
        
        Returns:
            List of game information dictionaries
        """
        games = []
        
        try:
            for filename in os.listdir(self.save_dir):
                if filename.endswith('.pgn'):
                    filepath = os.path.join(self.save_dir, filename)
                    
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            game = chess.pgn.read_game(f)
                        
                        if game:
                            games.append({
                                'filename': filename,
                                'filepath': filepath,
                                'white': game.headers.get('White', 'Unknown'),
                                'black': game.headers.get('Black', 'Unknown'),
                                'result': game.headers.get('Result', '*'),
                                'date': game.headers.get('Date', 'Unknown'),
                                'size': os.path.getsize(filepath)
                            })
                    except:
                        continue
        except Exception as e:
            print(f"Error listing games: {e}")
        
        # Sort by date (newest first)
        games.sort(key=lambda x: x['filename'], reverse=True)
        
        return games
    
    def delete_game(self, filepath: str) -> bool:
        """Delete a saved game"""
        try:
            os.remove(filepath)
            return True
        except Exception as e:
            print(f"Error deleting game: {e}")
            return False
    
    def export_to_string(self, board: chess.Board) -> str:
        """Export current game to PGN string"""
        game = chess.pgn.Game()
        
        # Add moves
        node = game
        for move in board.move_stack:
            node = node.add_variation(move)
        
        # Convert to string
        exporter = chess.pgn.StringExporter(headers=False)
        pgn_string = game.accept(exporter)
        
        return pgn_string
    
    def import_from_string(self, pgn_string: str) -> Optional[chess.Board]:
        """Import game from PGN string"""
        try:
            pgn = io.StringIO(pgn_string)
            game = chess.pgn.read_game(pgn)
            
            if game:
                board = game.board()
                for move in game.mainline_moves():
                    board.push(move)
                return board
        except Exception as e:
            print(f"Error importing game: {e}")
        
        return None


class AutoSaver:
    """Automatic game saving"""
    
    def __init__(self, game_saver: GameSaver):
        self.game_saver = game_saver
        self.autosave_enabled = True
        self.autosave_interval = 10  # Save every 10 moves
    
    def should_autosave(self, move_count: int) -> bool:
        """Check if game should be auto-saved"""
        return self.autosave_enabled and move_count % self.autosave_interval == 0
    
    def autosave(self, board: chess.Board, white: str, black: str):
        """Auto-save current game"""
        if not self.autosave_enabled:
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"autosave_{white}_vs_{black}_{timestamp}.pgn"
            filepath = os.path.join(self.game_saver.save_dir, filename)
            
            game = chess.pgn.Game()
            game.headers["White"] = white
            game.headers["Black"] = black
            game.headers["Date"] = datetime.now().strftime("%Y.%m.%d")
            game.headers["Event"] = "Autosave"
            
            node = game
            for move in board.move_stack:
                node = node.add_variation(move)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                exporter = chess.pgn.FileExporter(f)
                game.accept(exporter)
            
        except Exception as e:
            print(f"Autosave error: {e}")


# Global game saver instance
_game_saver = None

def get_game_saver() -> GameSaver:
    """Get global game saver instance"""
    global _game_saver
    if _game_saver is None:
        _game_saver = GameSaver()
    return _game_saver
