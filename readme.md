# 🧰 Code Station - IDE Web cho Python, C++ và Casio ROP

Web IDE đa năng hỗ trợ lập trình Python, C++, và Assembly cho máy tính Casio fx-580VNX.

## ✨ Tính năng

### 🐍 Python Tools
- Chạy code Python trực tiếp trong trình duyệt (Pyodide)
- Syntax highlighting giống PyCharm
- Hỗ trợ nhiều tab làm việc
- Lưu/load file .py
- AI chat assistant (Gemini)
- Chế độ Studio (hiện Input + Output cùng lúc)

### ⚙️ C++ Tools
- Chạy code C++ trong trình duyệt (JSCPP)
- Syntax highlighting
- Hỗ trợ cin/scanf (qua prompt)
- Lưu/load file .cpp
- AI chat assistant
- Multi-tab workspace

### 📟 Casio Tools (fx-580VNX ROP)
- **Compiler Assembly → HEX** (cần chạy server Python)
- Syntax highlighting cho Assembly
- Dịch ảnh thành hex (192x63, custom size)
- Pixel Editor & Bitmap Editor
- Dịch token (Hex → Token)
- Auto-assign hex vào payload ABC
- AI chat assistant chuyên về ROP
- Lưu/load file .asm

## 🚀 Cài đặt và Sử dụng

### Cách 1: Sử dụng Web (không cần server - ngoại trừ Casio Compiler)

1. Mở file `index.html` trong trình duyệt
2. Chọn công cụ bạn muốn: Python / C++ / Casio
3. Bắt đầu code!

**Lưu ý:** Các công cụ Python và C++ chạy hoàn toàn trên trình duyệt, không cần cài đặt gì thêm.

### Cách 2: Sử dụng Casio Compiler (cần server Python)

#### Bước 1: Cài đặt Python và dependencies

```bash
# Kiểm tra Python (cần version 3.8+)
python --version

# Cài đặt thư viện
pip install -r requirements.txt
```

#### Bước 2: Chạy server

**Windows:**
```bash
# Cách đơn giản nhất
run_server.bat

# Hoặc chạy trực tiếp
python compiler_server.py
```

**Linux/Mac:**
```bash
# Cấp quyền chạy
chmod +x run_server.sh

# Chạy server
./run_server.sh

# Hoặc chạy trực tiếp
python3 compiler_server.py
```

#### Bước 3: Sử dụng web

1. Giữ server chạy (không tắt terminal)
2. Mở `index.html` trong trình duyệt
3. Vào **Casio Tools**
4. Viết code Assembly
5. Bấm nút **Compiler**
6. Kết quả HEX sẽ hiện trong phần Output

## 📁 Cấu trúc thư mục

```
Web hỗ trợ/
├── index.html              # Web IDE chính
├── compiler_server.py      # Server Python cho Casio Compiler
├── requirements.txt        # Thư viện Python cần thiết
├── run_server.bat         # Script chạy nhanh (Windows)
├── run_server.sh          # Script chạy nhanh (Linux/Mac)
├── README.md              # File này
├── HƯỚNG_DẪN_CHẠY_COMPILER.md  # Hướng dẫn chi tiết
├── hdcompiler_vn/         # Compiler engine cho Casio
│   └── hdcompiler_vn/
│       ├── libcompiler.py      # Core compiler
│       ├── text.py             # Character table
│       ├── 580vnx/             # Data cho fx-580VNX
│       │   ├── gadgets         # ROP gadgets
│       │   ├── get_char_table.py
│       │   └── ...
│       └── 580vnx_ropchain/    # Ví dụ code ASM
└── index-backup.html      # Backup
```

## 🔧 Yêu cầu hệ thống

### Web IDE (Python/C++):
- Trình duyệt hiện đại (Chrome, Firefox, Edge, Safari)
- Kết nối internet (để tải Pyodide và JSCPP lần đầu)

### Casio Compiler Server:
- Python 3.8 trở lên
- Các thư viện: flask, flask-cors, colorama
- RAM: ~100MB
- Hệ điều hành: Windows/Linux/Mac

## 📖 Hướng dẫn sử dụng

### Python Tools
1. Viết code Python trong phần Input
2. Bấm **Chạy** (hoặc Ctrl+Enter)
3. Xem kết quả trong Output
4. Dùng nút **Studio** để xem cả Input và Output

### C++ Tools
1. Viết code C++ (hỗ trợ iostream, vector, string...)
2. Bấm **Chạy**
3. Nếu code có `cin` hoặc `scanf`, sẽ có popup nhập input
4. Xem kết quả trong Output

### Casio Tools - Compiler
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

### Casio Tools - Dịch ảnh
1. Click nút **Dịch ảnh** trong sidebar
2. Chọn tab "📷 Dịch ảnh"
3. Tải ảnh lên (khuyến khích ảnh đen trắng)
4. Kết quả hex sẽ hiện dưới ảnh

### Casio Tools - Pixel Editor
1. Tab "🎨 Pixel editor"
2. Nhập kích thước (width x height)
3. Bấm **Tạo** để tạo canvas
4. Vẽ pixel bằng chuột (chế độ Vẽ/Tẩy)
5. Hoặc **Dịch ảnh theo kích cỡ** để import ảnh

## 🤖 AI Assistant

Cả 3 tools đều có AI chat assistant (Gemini):
- Hỏi đáp về code
- Debug lỗi
- Giải thích thuật toán
- Gợi ý code

**Cách dùng:**
1. Click icon 🤖 trong sidebar
2. Gõ câu hỏi hoặc gửi file code
3. AI sẽ trả lời và giúp bạn

## ⚙️ Cài đặt

- **Theme:** Sáng / Xám / Tối
- **Tab size:** 2 / 4 / 8 spaces
- **Số dòng:** Bật/tắt line numbers
- **Màu code:** Bật/tắt syntax highlighting

Click icon ⚙️ trong sidebar để truy cập.

## 🐛 Xử lý lỗi

### Lỗi: "Compiler không hoạt động"
✅ **Giải pháp:**
1. Kiểm tra server đã chạy chưa: http://localhost:5000
2. Mở Console (F12) xem lỗi gì
3. Đọc `HƯỚNG_DẪN_CHẠY_COMPILER.md`

### Lỗi: "ModuleNotFoundError"
✅ **Giải pháp:**
```bash
pip install -r requirements.txt
```

### Lỗi: "Port 5000 đã được sử dụng"
✅ **Giải pháp:**
Sửa port trong `compiler_server.py` dòng cuối:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Lỗi Python/C++ không chạy
✅ **Giải pháp:**
- Kiểm tra kết nối internet
- Refresh lại trang (F5)
- Xóa cache trình duyệt

## 📝 Ví dụ Code

### Python - Hello World
```python
print("Hello, World!")
```

### C++ - Hello World
```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "Hello, World!" << endl;
    return 0;
}
```

### Casio ASM - Hello World
```assembly
org 0xe9e0
text:
    str "Hello World"
    0x00
```

## 🔗 Tài nguyên tham khảo

- [Pyodide Documentation](https://pyodide.org/)
- [JSCPP GitHub](https://github.com/felixhao28/JSCPP)
- [Casio fx-580VNX ROP Guide](./hdcompiler_vn/hdcompiler_vn/Guide.md)
- [Gemini API](https://ai.google.dev/)

## 📄 License

- Web IDE: Tự do sử dụng và chỉnh sửa
- hdcompiler_vn: Xem [LICENSE](./hdcompiler_vn/hdcompiler_vn/LICENSE)

## 👨‍💻 Credits

- **Web IDE**: Được phát triển dựa trên yêu cầu
- **Casio Compiler**: hdcompiler_vn by @Bashamee và contributors
- **Libraries**: Pyodide, JSCPP, Flask, Font Awesome

## 🆘 Hỗ trợ

Nếu gặp vấn đề:
1. Đọc `HƯỚNG_DẪN_CHẠY_COMPILER.md`
2. Kiểm tra Console log (F12)
3. Kiểm tra server log
4. Đảm bảo Python version >= 3.8

---

**Phiên bản:** 1.0  
**Ngày cập nhật:** 2026-09-04
