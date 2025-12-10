"""
Test script to verify all components work correctly
"""

import sys
import os

# Add paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all imports work"""
    print("🧪 Testing imports...")
    
    try:
        import chess
        print("✅ python-chess imported successfully")
    except ImportError as e:
        print(f"❌ python-chess import failed: {e}")
        return False
    
    try:
        from common import constants, protocol
        print("✅ common package imported successfully")
    except ImportError as e:
        print(f"❌ common package import failed: {e}")
        return False
    
    try:
        from server import chess_engine, game_manager
        print("✅ server package imported successfully")
    except ImportError as e:
        print(f"❌ server package import failed: {e}")
        return False
    
    try:
        from client.ui import board, styles, components
        print("✅ client.ui package imported successfully")
    except ImportError as e:
        print(f"❌ client.ui package import failed: {e}")
        return False
    
    try:
        from client.network import socket_handler
        print("✅ client.network package imported successfully")
    except ImportError as e:
        print(f"❌ client.network package import failed: {e}")
        return False
    
    return True


def test_chess_engine():
    """Test chess engine functionality"""
    print("\n🧪 Testing chess engine...")
    
    try:
        from server.chess_engine import ChessEngine
        
        engine = ChessEngine()
        print("✅ ChessEngine initialized")
        
        # Test initial position
        assert engine.get_current_turn() == "white"
        print("✅ Initial turn is white")
        
        # Test valid move
        assert engine.make_move("e2", "e4") == True
        print("✅ Valid move e2-e4 accepted")
        
        # Test turn switched
        assert engine.get_current_turn() == "black"
        print("✅ Turn switched to black")
        
        # Test invalid move
        assert engine.make_move("e7", "e5") == True
        print("✅ Valid move e7-e5 accepted")
        
        # Test legal moves
        legal_moves = engine.get_legal_moves("g1")
        assert len(legal_moves) > 0
        print(f"✅ Legal moves for g1: {legal_moves}")
        
        # Test piece at square
        piece = engine.get_piece_at("e4")
        assert piece == "P"
        print(f"✅ Piece at e4: {piece}")
        
        # Test piece color
        color = engine.get_piece_color("e4")
        assert color == "white"
        print(f"✅ Color at e4: {color}")
        
        return True
        
    except Exception as e:
        print(f"❌ Chess engine test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_game_manager():
    """Test game manager functionality"""
    print("\n🧪 Testing game manager...")
    
    try:
        from server.game_manager import GameManager, Player
        import socket
        
        manager = GameManager()
        print("✅ GameManager initialized")
        
        # Create mock socket
        mock_socket = None
        
        # Test create player
        player1 = Player("TestPlayer1", mock_socket, ("127.0.0.1", 1234))
        manager.add_player(player1)
        print("✅ Player created and added")
        
        # Test create room
        room = manager.create_room("Test Room", player1)
        assert room is not None
        print(f"✅ Room created: {room.room_id}")
        
        # Test get room
        retrieved_room = manager.get_room(room.room_id)
        assert retrieved_room == room
        print("✅ Room retrieved successfully")
        
        # Test available rooms
        rooms = manager.get_available_rooms()
        assert len(rooms) == 1
        print(f"✅ Available rooms: {len(rooms)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Game manager test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_protocol():
    """Test message protocol"""
    print("\n🧪 Testing protocol...")
    
    try:
        from common.protocol import create_message, parse_message
        
        # Test create message
        msg = create_message("TEST", {"data": "test_value"})
        print("✅ Message created")
        
        # Test parse message
        parsed = parse_message(msg)
        assert parsed["type"] == "TEST"
        assert parsed["data"]["data"] == "test_value"
        print("✅ Message parsed correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Protocol test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_ui_components():
    """Test UI components can be imported"""
    print("\n🧪 Testing UI components...")
    
    try:
        from client.ui.styles import COLORS, FONTS, get_button_style
        print("✅ Styles imported")
        
        assert "primary" in COLORS
        assert "title" in FONTS
        print("✅ Styles structure correct")
        
        btn_style = get_button_style("primary")
        assert "bg" in btn_style
        print("✅ Button style generated")
        
        return True
        
    except Exception as e:
        print(f"❌ UI components test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 Running Chess Game Tests")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Chess Engine", test_chess_engine()))
    results.append(("Game Manager", test_game_manager()))
    results.append(("Protocol", test_protocol()))
    results.append(("UI Components", test_ui_components()))
    
    print("\n" + "=" * 60)
    print("📊 Test Results")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{name:20s} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("=" * 60)
    print(f"Total: {passed + failed} | Passed: {passed} | Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed! System is ready to use.")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please fix errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
