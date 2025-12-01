#!/bin/bash
# OtakuVerse Startup Script for macOS/Linux

clear

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                   🎌 OtakuVerse 🎌                       ║"
echo "║     Multi-Agent Entertainment Recommendation System      ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "✗ ERROR: Python3 is not installed"
    echo "Please install Python 3.10+ from https://www.python.org/downloads/"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
    echo ""
fi

# Activate venv
source venv/bin/activate

# Check if requirements are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo "✓ Dependencies installed"
    echo ""
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your GOOGLE_API_KEY"
    echo "Opening .env file..."
    sleep 2
    if command -v nano &> /dev/null; then
        nano .env
    else
        vi .env
    fi
    echo ""
fi

# Main menu loop
while true; do
    clear
    echo ""
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                OtakuVerse - Main Menu                    ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo ""
    echo "1. Run CLI (Interactive Mode)"
    echo "2. Run API Server (FastAPI)"
    echo "3. Open API Documentation"
    echo "4. Exit"
    echo ""
    read -p "Enter your choice (1-4): " choice
    
    case $choice in
        1)
            clear
            echo "Running OtakuVerse CLI..."
            echo ""
            python main.py
            read -p "Press Enter to continue..."
            ;;
        2)
            clear
            echo "Starting OtakuVerse API Server..."
            echo ""
            python run_server.py
            read -p "Press Enter to continue..."
            ;;
        3)
            if command -v open &> /dev/null; then
                open http://localhost:8000/docs
            elif command -v xdg-open &> /dev/null; then
                xdg-open http://localhost:8000/docs
            else
                echo "Please open http://localhost:8000/docs in your browser"
            fi
            read -p "Press Enter to continue..."
            ;;
        4)
            echo ""
            echo "👋 Thank you for using OtakuVerse!"
            echo ""
            exit 0
            ;;
        *)
            echo "✗ Invalid choice. Please try again."
            sleep 2
            ;;
    esac
done
