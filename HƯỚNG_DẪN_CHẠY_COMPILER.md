# 🔧 Hướng Dẫn Chạy Casio Compiler Server

## 📋 Yêu cầu
- Python 3.8 trở lên
- Các thư viện trong file `requirements.txt`

## ⚙️ Cài đặt

### Bước 1: Cài đặt Python packages
Mở Command Prompt (CMD) hoặc PowerShell tại thư mục `D:\Dự án\Web hỗ trợ` và chạy:

```bash
pip install -r requirements.txt
```

Hoặc nếu có nhiều phiên bản Python:

```bash
python -m pip install -r requirements.txt
```

## 🚀 Chạy Server

### Cách 1: Chạy trực tiếp
```bash
python compiler_server.py
```

### Cách 2: Chạy với Python 3 (nếu có nhiều phiên bản)
```bash
python3 compiler_server.py
```

Sau khi chạy, bạn sẽ thấy:
```
==================================================
🚀 Casio Compiler Server
==================================================
📍 Server đang chạy tại: http://localhost:5000
📍 API endpoint: http://localhost:5000/compile
📍 Để dừng server: Nhấn Ctrl+C
==================================================
```

## 🌐 Sử dụng Web

1. **Giữ server chạy** (không tắt cửa sổ CMD/PowerShell)
2. Mở file `index.html` trong trình duyệt
3. Chọn **Casio tools**
4. Viết code ASM trong phần Input
5. Bấm nút **Compiler**
6. Kết quả sẽ hiện trong phần Output

## ✅ Kiểm tra Server

Mở trình duyệt và truy cập: http://localhost:5000

Bạn sẽ thấy trang chủ của server với trạng thái "Server đang chạy!"

## 🧪 Test thử Compiler

### Ví dụ 1: Hello World đơn giản
```assembly
org 0xe9e0
setup:
    setlr
    setsfr
    buffer_clear
inchu:
    xr0 = 0x3021 , adr_of text
    printline
    render.ddd4
text:
    str "Xin~chào"
    0x00
```

### Ví dụ 2: Test với label
```assembly
org 0xe9e0
text:
    str "Hello"
    0x00
```

## ❌ Xử lý lỗi

### Lỗi: "ModuleNotFoundError: No module named 'flask'"
**Giải pháp:** Chạy lại lệnh cài đặt:
```bash
pip install -r requirements.txt
```

### Lỗi: "Address already in use"
**Giải pháp:** 
- Port 5000 đang bị chiếm dụng
- Tìm và tắt tiến trình đang dùng port 5000
- Hoặc sửa port trong file `compiler_server.py` (dòng cuối cùng):
```python
app.run(host='0.0.0.0', port=5001, debug=True)  # Đổi sang port 5001
```

### Lỗi: "File not found: gadgets"
**Giải pháp:**
- Kiểm tra thư mục `hdcompiler_vn/hdcompiler_vn/580vnx/gadgets` có tồn tại không
- Đảm bảo cấu trúc thư mục đúng

### Lỗi: "CORS error" trong trình duyệt
**Giải pháp:**
- Đã được xử lý bởi `flask-cors`
- Nếu vẫn lỗi, mở file `index.html` bằng Live Server hoặc từ `http://localhost` thay vì `file://`

## 📝 Lưu ý

1. **Không tắt cửa sổ chạy server** khi đang sử dụng web
2. Server cần chạy trước khi mở web và sử dụng tính năng Compiler
3. Nếu sửa code server, cần khởi động lại server (Ctrl+C rồi chạy lại)
4. Server chạy ở chế độ debug, tự động reload khi có thay đổi

## 🔍 Debugging

Nếu compiler không hoạt động:

1. Kiểm tra Console của trình duyệt (F12)
2. Kiểm tra terminal đang chạy server xem có lỗi không
3. Test API trực tiếp bằng curl hoặc Postman:

```bash
curl -X POST http://localhost:5000/compile -H "Content-Type: application/json" -d "{\"code\":\"org 0xe9e0\\ntext:\\nstr \\\"test\\\"\"}"
```

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra Python version: `python --version` (cần >= 3.8)
2. Kiểm tra pip version: `pip --version`
3. Đọc lại log lỗi trong terminal
4. Kiểm tra file `text.py` và `get_char_table.py` trong thư mục `580vnx`
