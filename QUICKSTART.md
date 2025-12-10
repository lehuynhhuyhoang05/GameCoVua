# 🚀 Quick Start Guide

## Chạy Game Nhanh trong 3 Bước

### 📦 Bước 1: Cài Đặt (1 phút)

```bash
# Clone project
git clone https://github.com/lehuynhhuyhoang05/GameCoVua.git
cd GameCoVua

# Cài dependencies
pip install python-chess
```

### 🖥️ Bước 2: Start Server (5 giây)

Mở Terminal 1:
```bash
python server/main.py
```

Thấy thông báo này là OK:
```
♟️  Chess Server started on 127.0.0.1:5555
📡 Waiting for connections...
```

### 🎮 Bước 3: Chơi Game (2 phút)

#### Terminal 2 - Player 1:
```bash
python client/main_enhanced.py
```
1. Nhập: `Player1` → Login
2. Click: **➕ Create Room**
3. Nhập: `My Room` → Create
4. ⏳ Chờ Player 2...

#### Terminal 3 - Player 2:
```bash
python client/main_enhanced.py
```
1. Nhập: `Player2` → Login
2. Click: **🔄 Refresh**
3. Double-click phòng "My Room"
4. 🎉 Game bắt đầu!

---

## 🎯 Chơi Thế Nào?

### Di Chuyển
1. Click quân cờ → Highlight xanh lá
2. Click ô đích → Quân di chuyển

### Chiến Thắng
- Checkmate đối phương ✅
- Đối phương resign 🏳️
- Đối phương hết giờ ⏰

---

## ⚡ Shortcuts

| Phím | Chức năng |
|------|-----------|
| Enter | Gửi chat |
| Esc | Deselect quân |

---

## 🐛 Gặp Lỗi?

### ❌ "Could not connect to server"
```bash
# Kiểm tra server đã chạy chưa
python server/main.py
```

### ❌ "Username already taken"
→ Đổi username khác

### ❌ "ModuleNotFoundError: chess"
```bash
pip install python-chess
```

---

## 📸 Screenshots

### Login
![Login Screen](screenshots/login.png)

### Lobby
![Lobby](screenshots/lobby.png)

### Game
![Gameplay](screenshots/game.png)

---

## 🎨 UI Features

✨ **Có gì mới trong Enhanced version?**

- ⏱️ **Timer**: Đếm giờ cho mỗi người
- 📜 **Move History**: Lịch sử nước đi
- 🎖️ **Captured Pieces**: Quân bị bắt + điểm
- 👥 **Player Cards**: Thông tin người chơi
- 🎯 **Legal Moves**: Highlight nước đi hợp lệ
- 💬 **Enhanced Chat**: Chat với emoji
- 🎨 **Modern UI**: Giao diện đẹp Material Design

---

## 🔗 Links

- 📚 [Full Documentation](docs/SETUP.md)
- 💻 [Development Guide](docs/DEVELOPMENT.md)
- 🐛 [Report Issues](https://github.com/lehuynhhuyhoang05/GameCoVua/issues)
- ⭐ [Star on GitHub](https://github.com/lehuynhhuyhoang05/GameCoVua)

---

## 🎉 Chúc Bạn Chơi Vui!

Made with ❤️ by Nhóm 14
