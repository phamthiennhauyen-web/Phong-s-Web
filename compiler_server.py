#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Casio Compiler Server - Hỗ trợ web compile code ASM cho Casio fx-580VNX
Chạy file này, sau đó web sẽ gọi đến server để compile code
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os
import io
import traceback
import re
from contextlib import redirect_stdout, redirect_stderr

# Add hdcompiler_vn to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'hdcompiler_vn', 'hdcompiler_vn'))

# Import compiler modules
from libcompiler import (
    process, finish_processing,
    get_commands, set_font, set_npress_array, set_symbolrepr,
    canonicalize, del_inline_comment, to_lowercase,
    read_rename_list, get_rom
)
import libcompiler
import itertools

app = Flask(__name__)
CORS(app)  # Enable CORS for web requests

def init_580vnx_compiler():
    vnx_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hdcompiler_vn', 'hdcompiler_vn', '580vnx')
    old_cwd = os.getcwd()
    os.chdir(vnx_dir)
    try:
        sys.path.insert(0, vnx_dir)
        sys.path.insert(0, os.path.join(vnx_dir, '..'))
        get_rom('rom.bin')
        
        # Tạo disasm giả để bypass assertion trong read_rename_list
        libcompiler.disasm = ['rt'] * 0x40000
        
        get_commands('gadgets')
        try:
            read_rename_list('labels')
            read_rename_list(os.path.join('..', 'labels_sfr'))
        except Exception:
            pass # Không bắt buộc cho compile cơ bản

        FONT = [l.split('\t') for l in '''
															
𝒙	𝒚	𝒛	⋯	▲	▼	▸	 ˍ	$	◁	&	𝑡	ᴛ	ₜ	ₕ	₅
 	!	"	#	×	%	÷	'	(	)	⋅	+	,	—	.	/
0	1	2	3	4	5	6	7	8	9	:	;	<	=	>	?
@	A	B	C	D	E	F	G	H	I	J	K	L	M	N	O
P	Q	R	S	T	U	V	W	X	Y	Z	[	▫	]	^	_
-	a	b	c	d	e	f	g	h	i	j	k	l	m	n	o
p	q	r	s	t	u	v	w	x	y	z	{	|	}	~	⊢
𝐢	𝐞	x	⏨	∞	°	ʳ	ᵍ	∠	x̅	y̅	x̂	ŷ	→	∏	⇒
ₓ	⏨	⏨̄	⌟	≤	≠	≥	⇩	√	∫	ᴀ	ʙ	ᴄ	ₙ	▶	◀	
⁰	¹	²	³	⁴	⁵	⁶	⁷	⁸	⁹	⁻¹	ˣ	¹⁰	₍	₎	±	
₀	₁	₂	₋₁	ꜰ	ɴ	ᴘ	µ	𝐀	𝐁	𝐂	𝐃	𝐄	𝐅	𝐏	▷	
Σ	α	γ	ε	θ	λ	μ	π	σ	ϕ	ℓ	ℏ	█	⎕	₃	▂
𝐟	𝐩	𝐧	𝛍	𝐦	𝐤	𝐌	𝐆	𝐓	𝐏	𝐄	𝑭	ₚ	ₑ	ᴊ	ᴋ
τ	ᵤ	₉	Å	ₘ	ɪ	₄									
															
'''.strip('\n').split('\n')]
        assert len(FONT) == 16
        assert all(len(l) >= 16 for l in FONT)
        FONT = [*itertools.chain.from_iterable(l[:16] for l in FONT)]
        set_font(FONT)

        npress = (
            99,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,
            24,24,24,24,24,24,24,24,24,30,24,24,24,24,24,24,
            24,2 ,2 ,2 ,24,24,24,24,24,24,24,24,2 ,1 ,1 ,24,
            1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,24,24,24,24,24,24,
            2 ,1 ,2 ,2 ,2 ,2 ,2 ,2 ,1 ,2 ,2 ,2 ,24,24,24,24,
            2 ,1 ,2 ,2 ,24,24,24,24,24,24,24,24,24,24,24,49,
            1 ,49,49,49,49,49,49,49,2 ,2 ,49,49,3 ,3 ,3 ,3 ,
            3 ,3 ,2 ,2 ,1 ,1 ,2 ,1 ,1 ,1 ,2 ,2 ,2 ,1 ,2 ,2 ,
            49,49,49,2 ,2 ,49,49,2 ,2 ,2 ,49,49,49,49,49,49,
            49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,
            49,49,49,49,49,2 ,1 ,1 ,1 ,1 ,2 ,49,49,2 ,2 ,49,
            49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,
            1 ,49,49,49,49,49,49,49,1 ,1 ,2 ,49,49,49,49,49,
            1 ,49,49,49,1 ,1 ,2 ,2 ,2 ,3 ,3 ,3 ,1 ,3 ,3 ,3 ,
            3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,49,49,49,49,49,49,49,49,
            49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,
        )
        set_npress_array(npress)

        from get_char_table import f as get_symbol
        symbols = [
            ''.join(map(FONT.__getitem__, get_symbol(x)[1]))
            for x in range(0xf0)
        ] + ['@'] * 0x10
        set_symbolrepr(symbols[:])
    finally:
        os.chdir(old_cwd)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

print("Dang khoi tao Casio Compiler...")
init_580vnx_compiler()
print("Compiler da san sang!")

def compile_asm(source_code):
    """
    Compile ASM code and return result
    
    Args:
        source_code (str): ASM source code
        
    Returns:
        dict: Compilation result with success status and output
    """
    # Reset global variables for fresh compilation
    import libcompiler
    libcompiler.result = []
    libcompiler.labels = {}
    libcompiler.adr_of_cmds = []
    libcompiler.adr_arith_cmds = []
    libcompiler.pr_length_cmds = []
    libcompiler.end = []
    libcompiler.home = None
    libcompiler.in_comment = False
    libcompiler.string_vars = {}
    libcompiler.endaddr = ""
    
    try:
        # Process program line by line
        lines = source_code.split('\n')
        modified_program = []
        setup_loop_detected = False
        
        # Preprocess setup_loop
        for input_line in lines:
            line = canonicalize(del_inline_comment(input_line))
            if line.lower().startswith('setup_loop'):
                setup_loop_detected = True
                parts = line.split(',')
                if len(parts) == 2:
                    src = parts[0].split()[1].strip()
                    src_backup = parts[1].strip()
                    label = 'home'
                elif len(parts) == 3:
                    src = parts[0].split()[1].strip()
                    src_backup = parts[1].strip()
                    label = parts[2].strip() if parts[2].strip() != 'None' else 'home'
                else:
                    raise ValueError(f'Invalid setup_loop directive: {line}')
                    
                modified_code = f"""restore:
    setlr
    DI,RT
    xr0 = adr_of length, 0x01, 0x00
    [er0] = er2,rt
    qr0 = pr_length, {src_backup}, {src}, 0x0000
    0x8932
length:
    0x0800
    0x0000
set_sp:
    er6 = adr_of [-2] {label}
    sp = er6,pop er8"""
                modified_program.extend(modified_code.strip().split('\n'))
            else:
                modified_program.append(input_line)
        
        if not setup_loop_detected:
            modified_program = lines
        
        # Preprocess: Merge multi-line hex data
        # Khi gặp dòng "hex XX XX ...", nối các dòng tiếp theo chỉ chứa hex bytes
        preprocessed = []
        i = 0
        while i < len(modified_program):
            line = modified_program[i].strip()
            line_clean = canonicalize(del_inline_comment(line))
            
            # Nếu dòng này bắt đầu với 'hex'
            if line_clean.lower().startswith('hex'):
                hex_data = line_clean
                j = i + 1
                
                # Đọc tiếp các dòng sau chỉ chứa hex bytes
                while j < len(modified_program):
                    next_line = modified_program[j].strip()
                    if not next_line:  # Dòng trống
                        j += 1
                        continue
                    
                    next_clean = canonicalize(del_inline_comment(next_line))
                    
                    # Kiểm tra xem dòng tiếp theo có phải là label (có ':') hay lệnh mới không
                    if ':' in next_clean:
                        break
                    
                    # Kiểm tra xem có phải là lệnh mới không
                    keywords = ['hex', 'str', 'org', 'setup_loop', 'setlr', 'setsfr', 
                               'buffer_clear', 'render', 'xr0', 'er0', 'qr0', 'r0', 'r1', 
                               'push', 'pop', 'rt', 'di', 'ei', 'nop']
                    is_command = any(next_clean.lower().startswith(kw) for kw in keywords)
                    if is_command:
                        break
                    
                    # Kiểm tra xem có phải toàn hex bytes không (chỉ chứa 0-9, a-f, A-F, và khoảng trắng)
                    if re.match(r'^[0-9a-fA-F\s]+$', next_clean):
                        hex_data += ' ' + next_clean
                        j += 1
                    else:
                        break
                
                preprocessed.append(hex_data)
                i = j
            else:
                preprocessed.append(line)
                i += 1
        
        # Biến để lưu dòng đang xử lý (để hiển thị khi có lỗi)
        current_line_being_processed = None
        
        try:
            # Process each line
            for line_num, line in enumerate(preprocessed, 1):
                line = canonicalize(del_inline_comment(line))
                if not line.lower().startswith("str"):
                    line = to_lowercase(line)
                
                if line:
                    current_line_being_processed = line  # Lưu dòng hiện tại
                    process(line)
            
            # Finish processing (resolve labels, etc.)
            finish_processing()
            
            # Determine home address
            if libcompiler.home is None:
                if setup_loop_detected or 'loop' in libcompiler.labels:
                    libcompiler.home = 0xD730
                else:
                    libcompiler.home = 0xE9E0
            
            actual_home = libcompiler.home
            if 'home' in libcompiler.labels:
                actual_home = libcompiler.home - libcompiler.labels['home']
            
            # Resolve adr_of commands
            for source_adr, offset, target_label in libcompiler.adr_of_cmds:
                if target_label not in libcompiler.labels:
                    raise ValueError(f'Không tìm thấy nhãn (label): {target_label}')
                target_adr = actual_home + libcompiler.labels[target_label] + offset
                libcompiler.result[source_adr] = target_adr & 0xFF
                libcompiler.result[source_adr + 1] = (target_adr >> 8) & 0xFF
            
            # Format output
            start_addr = libcompiler.home
            end_addr = libcompiler.home + len(libcompiler.result)
            
            hex_bytes = ' '.join(f'{b:02x}' for b in libcompiler.result)
            
            # Create hex dump
            dump = []
            for idx in range(0, len(libcompiler.result), 16):
                chunk = libcompiler.result[idx:idx+16]
                chunk_hex = ' '.join(f'{b:02x}' for b in chunk)
                chunk_addr = f'0x{libcompiler.home + idx:04x}'
                dump.append(f'{chunk_addr}:  {chunk_hex}')
            
            # Labels info
            labels_info = ''
            if libcompiler.labels:
                labels_info = '\n📌 Vị trí các nhãn (Labels):\n'
                for lbl, off in libcompiler.labels.items():
                    labels_info += f'  • {lbl}: 0x{actual_home + off:04X} (+{off} bytes)\n'
            
            summary = f"""=== 0x{start_addr:04x} -> 0x{end_addr:04x} (Tổng: {len(libcompiler.result)} bytes) ===

📦 HEX ARRAY (Raw):
{hex_bytes}

📄 HEX DUMP:
{chr(10).join(dump)}{labels_info}"""
            
            return {
                'success': True,
                'output': summary,
                'rawHex': hex_bytes,
                'byteCount': len(libcompiler.result),
                'home': libcompiler.home
            }
            
        except Exception as e:
            # Lấy traceback đầy đủ
            tb_lines = traceback.format_exc()
            
            # Tạo output chi tiết (giống folder compiler gốc)
            # Thêm dòng "Trong lúc tao đang chạy dòng..." phía trước traceback
            if current_line_being_processed:
                error_output = f'''Trong lúc tao đang chạy dòng 
{current_line_being_processed}
{tb_lines}'''
            else:
                error_output = tb_lines
            
            return {
                'success': False,
                'error': str(e),
                'output': error_output
            }
        
    except Exception as outer_e:
        # Nếu có lỗi ở ngoài (setup phase), trả về lỗi đơn giản
        return {
            'success': False,
            'error': str(outer_e),
            'output': f'❌ Lỗi khởi tạo:\n{traceback.format_exc()}'
        }

@app.route('/')
def index():
    """Serve main HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (HTML, CSS, JS)"""
    return send_from_directory('.', path)

@app.route('/compile', methods=['POST'])
def compile_endpoint():
    """API endpoint to compile ASM code"""
    try:
        data = request.get_json()
        if not data or 'code' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing "code" field in request body'
            }), 400
        
        source_code = data['code']
        result = compile_asm(source_code)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'Compiler server is running',
        'version': '1.0'
    })

if __name__ == '__main__':
    print("\n" + "="*50)
    print("Casio Compiler Server")
    print("="*50)
    print("Server dang chay tai: http://localhost:5000")
    print("API endpoint: http://localhost:5000/compile")
    print("De dung server: Nhan Ctrl+C")
    print("="*50 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
