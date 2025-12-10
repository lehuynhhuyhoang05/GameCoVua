# ♟️ Chess Online - Multiplayer Chess Game

Game cờ vua trực tuyến sử dụng Python Socket Programming với giao diện Tkinter.

## 🚀 Tính Năng

- ✅ Multiplayer real-time qua Socket
- ✅ Đầy đủ luật cờ vua chuẩn
- ✅ Giao diện đồ họa với Tkinter
- ✅ Hệ thống phòng chơi
- ✅ Chat trong game
- ✅ Lưu lịch sử trận đấu

## 📋 Yêu Cầu

- Python 3.9+
- python-chess library

## 🔧 Cài Đặt

```bash
# Clone repository
git clone https://github.com/lehuynhhuyhoang05/GameCoVua.git
cd GameCoVua

# Cài đặt dependencies
pip install -r requirements.txt
```

## 🎮 Chạy Game

### Chạy Server:
```bash
python server/main.py
```

### Chạy Client:
```bash
python client/main.py
```

## 📁 Cấu Trúc Project

```
ChessGame/
├── server/           # Server-side code
│   ├── main.py      # Entry point server
│   ├── game_manager.py
│   └── chess_engine.py
├── client/          # Client-side code
│   ├── main.py     # Entry point client
│   ├── ui/         # Giao diện
│   └── network/    # Socket handling
├── common/         # Shared code
│   ├── protocol.py # Message protocol
│   └── constants.py
└── docs/           # Documentation
```

## 👥 Team

- Nhóm 14 - Lập Trình Mạng

## 📝 License

MIT License
