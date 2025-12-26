# Icon Placeholder

Đặt file icon của bạn vào đây với tên `icon.ico`

## Cách tạo icon:

### Option 1: Online Tool
1. Tạo logo tại: https://www.canva.com/
2. Export PNG (256x256)
3. Convert tại: https://convertio.co/png-ico/
4. Đổi tên thành `icon.ico`

### Option 2: Photoshop/GIMP
1. Design 256x256px
2. Export as ICO format
3. Save as `icon.ico`

### Option 3: Use Default
App sẽ dùng icon mặc định của Windows nếu không có file này.

## Đặt icon:
```
assets/
└── icon.ico  ← Đặt file ở đây
```

Sau đó build:
```bash
python build.py
```

Icon sẽ xuất hiện trên EXE file!
