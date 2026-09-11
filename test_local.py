#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test local để kiểm tra traceback có hoạt động không
"""

import sys
import os

# Add compiler to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'hdcompiler_vn', 'hdcompiler_vn'))

# Import compile function
from compiler_server import compile_asm

# Test code có lỗi
test_code = """org 0xe9e0
home:
 buffer_clear
 setl
 setsfr
"""

print("="*60)
print("TEST: Compiler với code có lỗi (setl)")
print("="*60)

result = compile_asm(test_code)

print("\n📋 SUCCESS:", result['success'])
print("\n📄 OUTPUT:")
print(result['output'])
print("\n" + "="*60)

# Kiểm tra
if 'Traceback' in result['output']:
    print("✅ PASS: Traceback được hiển thị")
else:
    print("❌ FAIL: Không có traceback")

if 'Trong lúc tao' in result['output'] or 'đang chạy dòng' in result['output']:
    print("✅ PASS: Có dòng 'Trong lúc tao đang chạy dòng'")
else:
    print("❌ FAIL: Không có dòng 'Trong lúc tao đang chạy dòng'")

if 'AssertionError' in result['output'] or 'Có lệnh này đâu má' in result['output']:
    print("✅ PASS: Có message lỗi")
else:
    print("❌ FAIL: Không có message lỗi")
