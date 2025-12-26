@echo off
echo ========================================
echo   Chess Online - Quick Build Script
echo ========================================
echo.

echo [1/4] Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

echo.
echo [2/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo [3/4] Building executable...
python build.py
if errorlevel 1 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo [4/4] Build complete!
echo.
echo ========================================
echo   SUCCESS!
echo ========================================
echo.
echo Output: dist\ChessOnline_Portable\
echo.
echo To run:
echo   1. Start server: Run_Server.bat
echo   2. Start client: ChessOnline.exe
echo.
pause
