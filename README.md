# ♟️ Chess Online - Multiplayer Chess Game

Game cờ vua trực tuyến sử dụng Python Socket Programming với giao diện Tkinter đẹp mắt.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

## 🎮 Demo & Screenshots

### Login Screen
![Login](docs/screenshots/login.png)

### Game Play
![Gameplay](docs/screenshots/gameplay.png)

## 🚀 Tính Năng

### ✨ Core Features
- ✅ **Real-time Multiplayer** - Chơi với bạn bè qua mạng
- ✅ **Full Chess Rules** - Đầy đủ luật cờ vua chuẩn quốc tế
- ✅ **Move Validation** - Kiểm tra nước đi hợp lệ
- ✅ **Check/Checkmate Detection** - Phát hiện chiếu/chiếu hết
- ✅ **Room System** - Tạo và tham gia phòng chơi

### 🎨 UI/UX Features
- 🎨 **Modern Beautiful UI** - Giao diện đẹp với Material Design
- 🎯 **Legal Moves Highlighting** - Highlight các nước đi hợp lệ
- 📜 **Move History** - Lịch sử nước đi với ký hiệu
- ⏱️ **Chess Timer** - Đồng hồ đếm ngược cho mỗi người
- 👥 **Player Cards** - Thông tin người chơi với rating
- 💬 **In-game Chat** - Chat trong game
- 🎖️ **Captured Pieces** - Hiển thị quân bị bắt
- ⚡ **Last Move Highlight** - Đánh dấu nước đi cuối

### 🔧 Technical Features
- 🔐 **Multi-threaded Server** - Server xử lý nhiều client
- 🌐 **JSON Protocol** - Giao thức truyền thông chuẩn
- 💾 **State Synchronization** - Đồng bộ trạng thái game
- 🛡️ **Error Handling** - Xử lý lỗi toàn diện

### 🆕 NEW - Enhanced Features
- 🔊 **Sound Effects** - Âm thanh cho mọi hành động
- 🎨 **10 Board Themes** - Classic, Dark, Neon, Wood...
- ⌨️ **Keyboard Shortcuts** - Điều khiển nhanh bằng phím tắt
- 🔔 **Desktop Notifications** - Thông báo desktop
- 🎬 **Smooth Animations** - Hiệu ứng di chuyển mượt mà
- 🤖 **AI Opponent** - Chơi với máy (3 độ khó)
- 💾 **Save/Load Games** - Lưu và load ván cờ (PGN format)
- 📦 **EXE Build** - Tạo file .exe chạy độc lập

## 📋 Yêu Cầu Hệ Thống

### Development Mode:
- **Python**: 3.8 trở lên
- **OS**: Windows, macOS, Linux
- **RAM**: 512MB trở lên
- **Network**: Kết nối mạng LAN/Internet

### EXE Mode (No Python needed!):
- **OS**: Windows 7/8/10/11
- **RAM**: 256MB trở lên
- **Network**: Kết nối mạng LAN/Internet

## 🔧 Cài Đặt

### Option A: Development (với Python)

#### 1. Clone Repository

```bash
git clone https://github.com/lehuynhhuyhoang05/GameCoVua.git
cd GameCoVua
```

#### 2. Cài Đặt Dependencies

```bash
pip install -r requirements.txt
```

Packages được cài:
- `python-chess` - Chess engine
- `pygame` - Sound effects  
- `numpy` - AI & audio
- `plyer` - Desktop notifications
- `pyinstaller` - Build EXE

### Option B: EXE Mode (KHÔNG CẦN Python!)

#### 1. Build EXE

```bash
# Quick build
quick_build.bat

# Or manual
python build.py
```

#### 2. Output

```
dist/ChessOnline_Portable/
├── ChessOnline.exe      ⭐ Chạy ngay không cần Python!
├── Run_Server.bat       🖥️ Server launcher
└── HOW_TO_RUN.txt      📝 Instructions
```

## 🎮 Cách Chạy

### 🅰️ Development Mode

#### Bước 1: Khởi động Server 🖥️

```bash
python server/main.py
```

Output:
```
♟️  Chess Server started on 127.0.0.1:5555
📡 Waiting for connections...
```

#### Bước 2: Chạy Client Enhanced 🎮

```bash
python client/main_enhanced.py
```

### 🅱️ EXE Mode (Portable)

#### Bước 1: Start Server

```bash
cd dist/ChessOnline_Portable
Double-click: Run_Server.bat
```

#### Bước 2: Start Client

```bash
Double-click: ChessOnline.exe
```

**Tính năng:**
- ✨ UI đẹp hiện đại
- ⏱️ Timer đầy đủ
- 📜 Move history
- 🎖️ Captured pieces
- 💬 Chat nâng cao

#### **Phiên bản Classic (Basic)**

```bash
python client/main.py
```

### Bước 3: Chơi Game 🎯

#### **Player 1:**
1. Nhập username (VD: "Player1")
2. Click **Login**
3. Click **➕ Create Room**
4. Nhập tên phòng
5. Chờ Player 2

#### **Player 2:**
1. Nhập username khác (VD: "Player2")
2. Click **Login**
3. Click **🔄 Refresh**
4. **Double-click** vào phòng
5. Game bắt đầu! 🎉

## 📖 Hướng Dẫn Chơi

### Di Chuyển Quân Cờ

1. **Click** vào quân cờ của bạn
2. Các ô hợp lệ sẽ được **highlight màu xanh**
3. **Click** vào ô đích để di chuyển

### Các Nút Điều Khiển

- **🏳 Resign**: Đầu hàng
- **🤝 Offer Draw**: Đề nghị hòa
- **🚪 Leave Game**: Rời khỏi game

### Kết Thúc Game

- **Checkmate** ♔: Chiếu hết → Thắng
- **Stalemate** 🤝: Hòa
- **Resign** 🏳️: Đầu hàng → Thua
- **Time Out** ⏰: Hết giờ → Thua

## 📁 Cấu Trúc Project

```
GameCoVua/
├── server/                 # Server-side code
│   ├── main.py            # Socket server
│   ├── chess_engine.py    # Chess logic (python-chess)
│   └── game_manager.py    # Room & player management
│
├── client/                # Client-side code
│   ├── main.py           # Basic client
│   ├── main_enhanced.py  # Enhanced client ⭐
│   ├── ui/
│   │   ├── board.py      # Chess board UI
│   │   ├── styles.py     # UI styles & colors
│   │   └── components.py # UI components (Timer, History, etc)
│   └── network/
│       └── socket_handler.py  # Network handler
│
├── common/               # Shared code
│   ├── constants.py     # Configuration
│   └── protocol.py      # Message protocol
│
├── docs/                # Documentation
│   ├── SETUP.md        # Setup guide
│   └── DEVELOPMENT.md  # Development guide
│
└── requirements.txt    # Dependencies
```

## ⚙️ Cấu Hình

### Thay Đổi Server Address

Edit `common/constants.py`:

```python
SERVER_HOST = '127.0.0.1'  # Localhost
SERVER_PORT = 5555         # Port
```

### Thay Đổi Timer

Edit `client/ui/components.py`:

```python
self.time_remaining = 600  # 10 minutes (600 seconds)
```

## 🐛 Troubleshooting

### ❌ "Could not connect to server"

**Giải pháp:**
```bash
# 1. Kiểm tra server đã chạy chưa
python server/main.py

# 2. Kiểm tra port 5555 có bị chiếm không
netstat -ano | findstr :5555

# 3. Tắt firewall hoặc cho phép port 5555
```

### ❌ "Username already taken"

**Giải pháp:**
- Dùng username khác
- Restart server nếu cần

### ❌ "No module named 'chess'"

**Giải pháp:**
```bash
pip install python-chess
```

### ❌ Move không được

**Giải pháp:**
- Kiểm tra xem có phải lượt của bạn không
- Chỉ được di chuyển quân màu của mình
- Nước đi phải hợp lệ theo luật cờ vua

## 🎯 Roadmap

### ✅ Phase 1 - Done
- [x] Basic multiplayer
- [x] Full chess rules
- [x] Chat system
- [x] Room management
- [x] Enhanced UI

### 🚧 Phase 2 - In Progress
- [ ] Pawn promotion dialog
- [ ] Sound effects
- [ ] Animation for moves
- [ ] Reconnection handling

### 📅 Phase 3 - Planned
- [ ] Game replay system
- [ ] ELO rating calculation
- [ ] Spectator mode
- [ ] Tournament mode

### 🔮 Phase 4 - Future
- [ ] AI opponent (Stockfish)
- [ ] Web version
- [ ] Mobile app
- [ ] Cloud deployment

## 🤝 Contributing

Contributions are welcome! 

1. Fork repository
2. Create feature branch: `git checkout -b feature/AmazingFeature`
3. Commit: `git commit -m 'feat: add some AmazingFeature'`
4. Push: `git push origin feature/AmazingFeature`
5. Open Pull Request

### Coding Standards

- Follow PEP 8
- Use conventional commits
- Add comments for complex logic
- Write docstrings for functions

## 📝 License

MIT License - Nhóm 14 - Lập Trình Mạng

## 👥 Team

**Nhóm 14 - Lập Trình Mạng**

- GitHub: [@lehuynhhuyhoang05](https://github.com/lehuynhhuyhoang05)
- Repository: [GameCoVua](https://github.com/lehuynhhuyhoang05/GameCoVua)

## 📞 Support

Nếu gặp vấn đề:

1. Check [Documentation](docs/)
2. Create [Issue](https://github.com/lehuynhhuyhoang05/GameCoVua/issues)
3. Contact team

## 🙏 Acknowledgments

- **python-chess** - Chess logic library
- **Tkinter** - GUI framework
- **Material Design** - UI inspiration

---

⭐ **Star this repo if you like it!**

Made with ❤️ by Nhóm 14
