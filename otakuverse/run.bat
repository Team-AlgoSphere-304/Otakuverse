@echo off
REM OtakuVerse Startup Script for Windows
REM This script sets up and runs the OtakuVerse application

setlocal enabledelayedexpansion

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                   🎌 OtakuVerse 🎌                       ║
echo ║     Multi-Agent Entertainment Recommendation System      ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✓ Python found
echo.

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
    echo.
)

REM Activate venv
call venv\Scripts\activate.bat

REM Check if requirements are installed
pip list | findstr "google-adk fastapi" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ✗ Failed to install dependencies
        pause
        exit /b 1
    )
    echo ✓ Dependencies installed
    echo.
)

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env >nul 2>&1
    echo.
    echo ⚠️  IMPORTANT: Edit .env file and add your GOOGLE_API_KEY
    echo Opening .env file...
    timeout /t 2 /nobreak
    notepad .env
    echo.
)

REM Menu
:menu
cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                OtakuVerse - Main Menu                    ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo 1. Run CLI (Interactive Mode)
echo 2. Run API Server (FastAPI)
echo 3. Open API Documentation
echo 4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    cls
    echo Running OtakuVerse CLI...
    echo.
    python main.py
    pause
    goto menu
)

if "%choice%"=="2" (
    cls
    echo Starting OtakuVerse API Server...
    echo.
    python run_server.py
    pause
    goto menu
)

if "%choice%"=="3" (
    start http://localhost:8000/docs
    echo Opened API documentation in your browser
    echo.
    timeout /t 2 /nobreak
    goto menu
)

if "%choice%"=="4" (
    echo.
    echo 👋 Thank you for using OtakuVerse!
    echo.
    exit /b 0
)

echo.
echo ✗ Invalid choice. Please try again.
timeout /t 2 /nobreak
goto menu
