# 🔧 Hướng Dẫn Development

## 🏗️ Kiến Trúc Hệ Thống

### Server Architecture

```
ChessServer (main.py)
├── GameManager (game_manager.py)
│   ├── Quản lý Room
│   ├── Quản lý Player
│   └── Matching logic
└── ChessEngine (chess_engine.py)
    ├── Board state
    ├── Move validation
    └── Game rules
```

### Client Architecture

```
ChessClient (main.py)
├── NetworkHandler (socket_handler.py)
│   └── Socket communication
└── UI Components
    └── ChessBoardUI (board.py)
        ├── Board rendering
        └── User interaction
```

## 📡 Message Protocol

### Client → Server

```json
{
  "type": "MSG_TYPE",
  "timestamp": "ISO-8601",
  "data": {
    // Message-specific data
  }
}
```

### Message Types

#### Authentication
- `LOGIN`: Login request
- `LOGOUT`: Logout request

#### Room Management
- `CREATE_ROOM`: Create new room
- `JOIN_ROOM`: Join existing room
- `LIST_ROOMS`: Get available rooms

#### Gameplay
- `MOVE`: Make a chess move
- `RESIGN`: Resign from game
- `OFFER_DRAW`: Offer draw
- `ACCEPT_DRAW`: Accept draw offer
- `DECLINE_DRAW`: Decline draw offer

#### Communication
- `CHAT`: Send chat message

### Server → Client

- `LOGIN_SUCCESS/FAILED`: Login response
- `ROOM_LIST`: Available rooms
- `ROOM_JOINED`: Successfully joined room
- `GAME_START`: Game started
- `MOVE_UPDATE`: Move made by player
- `GAME_OVER`: Game ended
- `CHAT_MESSAGE`: Chat message
- `ERROR`: Error message

## 🎨 UI Components

### ChessBoardUI

**Methods:**
- `set_position(fen)`: Set board from FEN
- `select_square(row, col)`: Select square
- `highlight_squares(squares)`: Highlight legal moves
- `coords_to_square(row, col)`: Convert coordinates
- `set_click_callback(callback)`: Handle clicks

### Color Scheme

- Light squares: `#F0D9B5`
- Dark squares: `#B58863`
- Highlight: `#FFFF00`
- Selected: `#00FF00`

## 🧪 Testing

### Test Server

```bash
python server/main.py
```

### Test Client (Multiple Instances)

Terminal 1:
```bash
python client/main.py
```

Terminal 2:
```bash
python client/main.py
```

### Test Scenarios

1. **Login Flow**
   - Valid username → Success
   - Duplicate username → Error
   - Empty username → Error

2. **Room Management**
   - Create room → Success
   - Join available room → Success
   - Join full room → Error

3. **Gameplay**
   - Valid move → Board updates
   - Invalid move → Error message
   - Not your turn → Error message

4. **Game End**
   - Checkmate → Winner declared
   - Resign → Opponent wins
   - Stalemate → Draw

## 🔐 Security Considerations

1. **Input Validation**
   - Validate all user inputs
   - Check move legality server-side
   - Prevent injection attacks

2. **Session Management**
   - One session per username
   - Automatic cleanup on disconnect

3. **Future Improvements**
   - Add password authentication
   - Implement TLS/SSL
   - Add rate limiting

## 📝 Coding Standards

### Python Style Guide

Follow PEP 8:
- Indent: 4 spaces
- Line length: 100 characters
- Naming: `snake_case` for functions/variables

### Git Commit Convention

Format: `<type>(<scope>): <subject>`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style
- `refactor`: Code refactoring
- `test`: Tests
- `chore`: Build/config

Example:
```bash
git commit -m "feat(server): add timer functionality"
```

## 🚀 Future Enhancements

### Phase 1 (Current)
- ✅ Basic multiplayer
- ✅ Full chess rules
- ✅ Chat system

### Phase 2 (Planned)
- ⏰ Timer/Clock
- 📊 Move history display
- 🎯 Legal move highlighting
- ♟️ Pawn promotion UI

### Phase 3 (Future)
- 💾 Game replay
- 📈 ELO rating system
- 👥 Spectator mode
- 🏆 Leaderboard

### Phase 4 (Advanced)
- 🤖 AI opponent
- 🌐 Web version
- 📱 Mobile app
- ☁️ Cloud deployment

## 🛠️ Development Tools

### Recommended IDEs
- VS Code
- PyCharm
- Sublime Text

### Useful Extensions (VS Code)
- Python
- Pylance
- Git Graph
- Better Comments

### Dependencies
- `python-chess`: Chess logic
- `tkinter`: GUI (built-in)

## 📚 Resources

### Chess Programming
- [Python-chess Documentation](https://python-chess.readthedocs.io/)
- [Chess Programming Wiki](https://www.chessprogramming.org/)

### Socket Programming
- [Python Socket Tutorial](https://realpython.com/python-sockets/)
- [Threading in Python](https://docs.python.org/3/library/threading.html)

### Tkinter GUI
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [TkDocs](https://tkdocs.com/)

## 🤝 Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'feat: add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📧 Contact

Nhóm 14 - Lập Trình Mạng
GitHub: https://github.com/lehuynhhuyhoang05/GameCoVua
