@echo off
echo ================================================
echo    Casio Compiler Server - Khoi dong nhanh
echo ================================================
echo.
echo Dang kiem tra Python...
python --version
if errorlevel 1 (
    echo [ERROR] Python chua duoc cai dat!
    echo Vui long cai dat Python tu https://www.python.org/
    pause
    exit /b 1
)
echo.
echo Dang kiem tra cac thu vien...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo [CANH BAO] Chua cai dat Flask!
    echo Dang tu dong cai dat...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Cai dat that bai!
        pause
        exit /b 1
    )
)
echo.
echo [OK] Moi thu da san sang!
echo ================================================
echo.
echo Dang khoi dong server...
echo Sau khi server chay, mo file index.html trong trinh duyet
echo Nhan Ctrl+C de dung server
echo.
echo ================================================
python compiler_server.py
pause
