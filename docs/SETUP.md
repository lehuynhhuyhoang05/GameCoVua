# 🎮 Hướng Dẫn Chạy Game Cờ Vua Online

## 📋 Yêu Cầu Hệ Thống

- Python 3.9 trở lên
- pip (Python package manager)
- Git

## 🔧 Cài Đặt

### 1. Clone Repository

```bash
git clone https://github.com/lehuynhhuyhoang05/GameCoVua.git
cd GameCoVua
```

### 2. Cài Đặt Dependencies

```bash
pip install -r requirements.txt
```

Hoặc cài đặt thủ công:
```bash
pip install python-chess
```

## 🚀 Chạy Game

### Bước 1: Khởi động Server

Mở terminal/cmd và chạy:

```bash
python server/main.py
```

Bạn sẽ thấy:
```
♟️  Chess Server started on 127.0.0.1:5555
📡 Waiting for connections...
```

### Bước 2: Khởi động Client (Player 1)

Mở terminal/cmd **MỚI** và chạy:

```bash
python client/main.py
```

1. Nhập username (ví dụ: "Player1")
2. Click **Login**
3. Click **Create Room**
4. Nhập tên phòng (ví dụ: "Room 1")
5. Chờ người chơi thứ 2

### Bước 3: Khởi động Client (Player 2)

Mở terminal/cmd **MỚI** (thứ 3) và chạy:

```bash
python client/main.py
```

1. Nhập username khác (ví dụ: "Player2")
2. Click **Login**
3. Click **Refresh Rooms** để xem danh sách phòng
4. **Double-click** vào phòng để tham gia
5. Game bắt đầu!

## 🎯 Cách Chơi

### Di Chuyển Quân Cờ

1. **Click** vào quân cờ bạn muốn di chuyển (quân màu trắng đi trước)
2. Ô sẽ được highlight màu xanh lá
3. **Click** vào ô đích để di chuyển
4. Nước đi sẽ được gửi đến server và cập nhật cho cả 2 người chơi

### Chat

- Nhập tin nhắn vào ô chat bên phải
- Nhấn **Enter** hoặc click **Send**

### Kết Thúc Game

- **Resign**: Click nút "Resign" để đầu hàng
- **Offer Draw**: Click "Offer Draw" để đề nghị hòa
- **Checkmate**: Game tự động kết thúc khi chiếu hết
- **Stalemate**: Game hòa khi không có nước đi hợp lệ

## 📁 Cấu Trúc Project

```
GameCoVua/
├── server/
│   ├── main.py              # Server chính
│   ├── chess_engine.py      # Logic cờ vua
│   └── game_manager.py      # Quản lý phòng & người chơi
├── client/
│   ├── main.py              # Client chính
│   ├── ui/
│   │   └── board.py         # Giao diện bàn cờ
│   └── network/
│       └── socket_handler.py # Socket client
├── common/
│   ├── constants.py         # Hằng số
│   └── protocol.py          # Giao thức message
└── requirements.txt
```

## ⚙️ Cấu Hình

Để thay đổi địa chỉ server, sửa file `common/constants.py`:

```python
SERVER_HOST = '127.0.0.1'  # Địa chỉ server
SERVER_PORT = 5555         # Port
```

## 🐛 Troubleshooting

### Lỗi: "Could not connect to server"

- Đảm bảo server đã được khởi động trước
- Kiểm tra port 5555 không bị chiếm bởi ứng dụng khác

### Lỗi: "Username already taken"

- Mỗi client phải dùng username khác nhau
- Restart server nếu cần

### Lỗi: "No module named 'chess'"

```bash
pip install python-chess
```

### Game bị lag hoặc không phản hồi

- Kiểm tra kết nối mạng
- Restart cả server và client

## 🎮 Demo Video

[Link video demo sẽ được thêm sau]

## 📞 Hỗ Trợ

Nếu gặp vấn đề, tạo issue trên GitHub:
https://github.com/lehuynhhuyhoang05/GameCoVua/issues

## 📝 License

MIT License - Nhóm 14 - Lập Trình Mạng
