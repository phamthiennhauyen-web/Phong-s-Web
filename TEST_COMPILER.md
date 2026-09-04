# Test Casio Compiler

Đây là file test để kiểm tra compiler có hoạt động không.

## Test 1: Code đơn giản

```assembly
org 0xe9e0
text:
str "abcd"
```

**Kết quả mong đợi:** Compile thành công và trả về hex

## Test 2: Code với label

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

**Kết quả mong đợi:** Compile thành công với labels

## Test 3: Code với comment

```assembly
# This is a comment
org 0xe9e0
text:
    str "test" # inline comment
    0x00
```

**Kết quả mong đợi:** Comment bị bỏ qua, compile thành công

## Cách test:

1. Chạy server:
   ```
   python compiler_server.py
   ```

2. Mở index.html

3. Vào Casio Tools

4. Copy từng đoạn code test ở trên vào Input

5. Bấm "Compiler"

6. Kiểm tra Output có kết quả hex không

## Test API trực tiếp (không dùng web):

```bash
curl -X POST http://localhost:5000/compile ^
  -H "Content-Type: application/json" ^
  -d "{\"code\":\"org 0xe9e0\ntext:\nstr \\\"test\\\"\"}"
```

Kết quả sẽ là JSON với field `success: true` và `output` chứa hex.
