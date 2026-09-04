#!/bin/bash

echo "================================================"
echo "   Casio Compiler Server - Quick Start"
echo "================================================"
echo ""
echo "Checking Python..."
python3 --version || python --version
if [ $? -ne 0 ]; then
    echo "[ERROR] Python is not installed!"
    echo "Please install Python from https://www.python.org/"
    exit 1
fi
echo ""
echo "Checking dependencies..."
pip3 show flask > /dev/null 2>&1 || pip show flask > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "[WARNING] Flask is not installed!"
    echo "Installing dependencies..."
    pip3 install -r requirements.txt || pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Installation failed!"
        exit 1
    fi
fi
echo ""
echo "[OK] Everything is ready!"
echo "================================================"
echo ""
echo "Starting server..."
echo "After server starts, open index.html in your browser"
echo "Press Ctrl+C to stop the server"
echo ""
echo "================================================"
python3 compiler_server.py || python compiler_server.py
