# 🌐 Hướng Dẫn Chơi Multiplayer Qua Mạng

## 🏠 Chơi Cùng WiFi (LAN) - SIÊU ĐƠN GIẢN

### ✅ Yêu Cầu:
- Cả 2 máy **kết nối cùng 1 WiFi/mạng LAN**
- Tắt Firewall hoặc cho phép Python

---

## 🎮 Cách Chơi - 3 Bước

### 📍 Bước 1: Máy Host - Xem IP của bạn

**Windows:**
```bash
ipconfig
```
Tìm dòng **IPv4 Address**, ví dụ: `192.168.1.100`

**Linux/Mac:**
```bash
ifconfig
# hoặc
ip addr
```

---

### 🖥️ Bước 2: Máy Host - Start Server

```bash
cd GameCoVua
python server/main.py
```

Thấy dòng này là OK:
```
♟️  Chess Server started on 0.0.0.0:5555
📡 Waiting for connections...
```

✅ Server đã sẵn sàng cho cả localhost VÀ LAN!

---

### 🎯 Bước 3: Cả 2 Máy - Start Client & Chơi

#### **Máy Host (người mở server):**
```bash
python client/main_enhanced.py
```
- **Server IP:** Nhập `127.0.0.1` (localhost)
- **Username:** Nhập tên, ví dụ: `Player1`
- Click **Login**
- Click **➕ Create Room** → Nhập tên phòng → Create
- ⏳ Đợi bạn...

#### **Máy Bạn (người join):**
```bash
python client/main_enhanced.py
```
- **Server IP:** Nhập IP của máy host, ví dụ: `192.168.1.100`
- **Username:** Nhập tên, ví dụ: `Player2`  
- Click **Login**
- Click **🔄 Refresh**
- Double-click vào phòng của bạn
- 🎉 **Bắt đầu chơi!**

---

## 🎊 VẬY LÀ XONG!

**Không cần sửa code gì cả!** Chỉ cần:
1. Host start server
2. Cả 2 nhập đúng IP khi login
3. Chơi!

---

## 🌍 Cách 2: Chơi Qua Internet (Xa Nhau)

### Yêu Cầu:
- Máy host có **IP Public** hoặc dùng **Ngrok**

### Dùng Ngrok (Miễn Phí):

#### 1. Cài Ngrok:
- Download: https://ngrok.com/download
- Đăng ký tài khoản free

#### 2. Máy Host chạy:
```bash
# Terminal 1: Start server
python server/main.py

# Terminal 2: Tunnel với ngrok
ngrok tcp 5555
```

Ngrok sẽ cho URL dạng:
```
Forwarding: tcp://0.tcp.ngrok.io:12345 -> localhost:5555
```

#### 3. Máy Bạn connect:
Sửa `client/network/socket_handler.py`:
```python
self.host = '0.tcp.ngrok.io'  # Domain từ ngrok
self.port = 12345              # Port từ ngrok
```

---

## 🛡️ Fix Firewall Windows

Nếu không connect được:

### Cách 1: Tạm tắt Firewall
1. Settings → Windows Security → Firewall
2. Tắt tạm "Private networks"

### Cách 2: Cho Python qua Firewall
1. Windows Defender Firewall → Advanced Settings
2. Inbound Rules → New Rule
3. Program → Browse → Chọn `python.exe`
4. Allow connection
5. Apply cho Private networks

---

## ✅ Kiểm Tra Kết Nối

### Test từ máy bạn:
```bash
# Windows
telnet 192.168.1.100 5555

# Hoặc dùng Python
python -c "import socket; s=socket.socket(); s.connect(('192.168.1.100', 5555)); print('OK')"
```

Nếu connect được → OK!

---

## 🎮 Bắt Đầu Chơi

### Máy Host:
1. Login → Create Room → "My Game"
2. Đợi bạn join

### Máy Bạn:
1. Login → Refresh
2. Double-click room "My Game"
3. 🎉 Chơi!

---

## 🐛 Troubleshooting

### Lỗi "Connection refused"
- ✅ Check cả 2 máy cùng WiFi
- ✅ Check IP đúng (`ipconfig`)
- ✅ Check server đang chạy
- ✅ Check Firewall

### Lỗi "Connection timeout"
- ✅ Ping thử: `ping 192.168.1.100`
- ✅ Tắt Firewall thử
- ✅ Restart server

### Game lag/chậm
- ✅ Check WiFi signal
- ✅ Đóng app tốn mạng khác
- ✅ Dùng dây LAN nếu có

---

## 📝 Notes

- **IP Private (192.168.x.x)**: Chỉ work trong cùng WiFi
- **Ngrok**: Tốt cho demo, nhưng có thể lag
- **Port 5555**: Có thể đổi nếu bị conflict

---

## 🎉 Chúc Chơi Vui!

Có vấn đề? Báo issue: https://github.com/lehuynhhuyhoang05/GameCoVua/issues
