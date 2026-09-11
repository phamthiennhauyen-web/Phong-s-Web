#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script để kiểm tra 2 tính năng đã sửa:
1. Hiển thị đầy đủ traceback khi compiler báo lỗi
2. Parse hex có xuống dòng trong code Assembly
"""

import requests
import json

COMPILER_URL = 'http://localhost:5000/compile'

def test_error_traceback():
    """Test 1: Kiểm tra hiển thị traceback đầy đủ khi có lỗi"""
    print("\n" + "="*60)
    print("TEST 1: Kiểm tra traceback khi compile code có lỗi")
    print("="*60)
    
    # Code có lỗi: lệnh "setl" không tồn tại (đúng phải là "setlr")
    code_with_error = """org 0xe9e0
home:
 buffer_clear
 setl
 setsfr
"""
    
    try:
        response = requests.post(COMPILER_URL, json={'code': code_with_error})
        result = response.json()
        
        if result['success']:
            print("❌ TEST FAILED: Code có lỗi nhưng compile thành công?!")
        else:
            print("✅ Compiler đã phát hiện lỗi")
            print("\n📋 OUTPUT:")
            print(result['output'])
            
            # Kiểm tra xem có traceback không
            if 'Traceback' in result['output']:
                print("\n✅ TEST PASSED: Traceback đầy đủ đã được hiển thị!")
            else:
                print("\n⚠️ TEST WARNING: Không tìm thấy traceback trong output")
    except Exception as e:
        print(f"❌ TEST ERROR: {e}")

def test_multiline_hex():
    """Test 2: Kiểm tra parse hex có xuống dòng"""
    print("\n" + "="*60)
    print("TEST 2: Kiểm tra parse hex có xuống dòng")
    print("="*60)
    
    # Code có hex xuống dòng (như ví dụ bạn đã cho)
    code_multiline_hex = """org 0xe9e0
home:
 buffer_clear
 setlr
 setsfr
anh:
 xr0 = hex 38 18 63 63
 render_bitmap
 er0 = adr_of img
 render.ddd
img:
 hex 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 3F F0 00 00 00
00 00 00 C0 0C 00 00 00
00 00 03 00 03 00 00 00
"""
    
    try:
        response = requests.post(COMPILER_URL, json={'code': code_multiline_hex})
        result = response.json()
        
        if result['success']:
            print("✅ Compiler thành công!")
            print(f"\n📊 Kết quả: {result['byteCount']} bytes")
            print("\n📦 HEX OUTPUT (đầu tiên 200 ký tự):")
            print(result['output'][:200] + "...")
            print("\n✅ TEST PASSED: Hex có xuống dòng đã được parse thành công!")
        else:
            print("❌ TEST FAILED: Compiler báo lỗi")
            print("\n📋 ERROR OUTPUT:")
            print(result['output'])
    except Exception as e:
        print(f"❌ TEST ERROR: {e}")

def test_server_health():
    """Kiểm tra server có đang chạy không"""
    print("\n" + "="*60)
    print("Kiểm tra kết nối với Compiler Server...")
    print("="*60)
    
    try:
        response = requests.get('http://localhost:5000/health', timeout=2)
        if response.status_code == 200:
            print("✅ Server đang chạy!")
            return True
        else:
            print(f"⚠️ Server trả về status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Không thể kết nối với server!")
        print("💡 Hãy chạy: python compiler_server.py")
        return False
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

if __name__ == '__main__':
    print("\n" + "🧪 BẮT ĐẦU KIỂM TRA COMPILER".center(60, "="))
    
    # Kiểm tra server trước
    if not test_server_health():
        print("\n❌ Không thể chạy test vì server chưa khởi động!")
        print("💡 Hướng dẫn:")
        print("   1. Mở terminal mới")
        print("   2. Chạy: python compiler_server.py")
        print("   3. Quay lại terminal này và chạy lại script test")
        exit(1)
    
    # Chạy các test
    test_error_traceback()
    test_multiline_hex()
    
    print("\n" + "🎉 HOÀN TẤT KIỂM TRA".center(60, "="))
    print()
