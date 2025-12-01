#!/usr/bin/env pwsh
# OtakuVerse Installation & Running Guide for PowerShell

Write-Host "`n"
Write-Host "╔════════════════════════════════════════════════════════════╗"
Write-Host "║                  🎌 OtakuVerse 🎌                          ║"
Write-Host "║      Multi-Agent Entertainment Recommendation System      ║"
Write-Host "╚════════════════════════════════════════════════════════════╝`n"

# Configuration
$ProjectPath = Get-Location
$VenvPath = Join-Path $ProjectPath "venv"

function Test-PythonInstalled {
    try {
        $version = python --version 2>&1
        Write-Host "✓ Python found: $version" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "✗ Python not found. Please install Python 3.10+" -ForegroundColor Red
        return $false
    }
}

function Initialize-VirtualEnv {
    if (-not (Test-Path $VenvPath)) {
        Write-Host "Creating virtual environment..." -ForegroundColor Cyan
        python -m venv $VenvPath
        Write-Host "✓ Virtual environment created" -ForegroundColor Green
    }
    else {
        Write-Host "✓ Virtual environment exists" -ForegroundColor Green
    }
}

function Activate-VirtualEnv {
    $activateScript = Join-Path $VenvPath "Scripts" "Activate.ps1"
    & $activateScript
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
}

function Install-Dependencies {
    Write-Host "`nInstalling dependencies..." -ForegroundColor Cyan
    pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Dependencies installed" -ForegroundColor Green
    }
    else {
        Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
        return $false
    }
    return $true
}

function Setup-Environment {
    $envFile = Join-Path $ProjectPath ".env"
    
    if (-not (Test-Path $envFile)) {
        Write-Host "`nSetting up .env file..." -ForegroundColor Cyan
        Copy-Item ".env.example" ".env"
        Write-Host "✓ .env file created" -ForegroundColor Green
        Write-Host "`n⚠️  IMPORTANT: Edit .env and add your GOOGLE_API_KEY" -ForegroundColor Yellow
        Write-Host "   Opening .env in Notepad in 3 seconds..." -ForegroundColor Yellow
        Start-Sleep -Seconds 3
        notepad ".env"
    }
    else {
        Write-Host "✓ .env file exists" -ForegroundColor Green
    }
}

function Show-Menu {
    Write-Host "`n" -ForegroundColor Cyan
    Write-Host "╔════════════════════════════════════════════════════════════╗"
    Write-Host "║                   Main Menu                                ║"
    Write-Host "╚════════════════════════════════════════════════════════════╝`n"
    Write-Host "1. Run CLI (Interactive Mode)" -ForegroundColor Cyan
    Write-Host "2. Run API Server (FastAPI)" -ForegroundColor Cyan
    Write-Host "3. Open API Documentation" -ForegroundColor Cyan
    Write-Host "4. Install/Update Dependencies" -ForegroundColor Cyan
    Write-Host "5. View Project Structure" -ForegroundColor Cyan
    Write-Host "6. Exit" -ForegroundColor Cyan
    Write-Host ""
}

function Run-CLI {
    Write-Host "`nRunning OtakuVerse CLI...`n" -ForegroundColor Green
    python main.py
}

function Run-Server {
    Write-Host "`nStarting OtakuVerse API Server...`n" -ForegroundColor Green
    Write-Host "API will be available at: http://localhost:8000`n" -ForegroundColor Yellow
    python run_server.py
}

function Show-Structure {
    Write-Host "`n" -ForegroundColor Cyan
    Write-Host "Project Structure:" -ForegroundColor Cyan
    Write-Host "──────────────────────────────────────────"
    
    Get-ChildItem -Path $ProjectPath -Directory | Where-Object { $_.Name -notin @('venv', '.git', '__pycache__') } | ForEach-Object {
        Write-Host "├── $($_.Name)/" -ForegroundColor Yellow
        Get-ChildItem -Path $_.FullName -File -Recurse | Select-Object -First 5 | ForEach-Object {
            Write-Host "│   ├── $($_.Name)" -ForegroundColor White
        }
        $count = (Get-ChildItem -Path $_.FullName -File -Recurse | Measure-Object).Count
        if ($count -gt 5) {
            Write-Host "│   └── ... and $($count - 5) more files" -ForegroundColor Gray
        }
    }
    
    Write-Host "│" -ForegroundColor White
    Write-Host "├── main.py" -ForegroundColor Yellow
    Write-Host "├── run_server.py" -ForegroundColor Yellow
    Write-Host "├── requirements.txt" -ForegroundColor Yellow
    Write-Host "├── .env" -ForegroundColor Yellow
    Write-Host "├── README.md" -ForegroundColor Yellow
    Write-Host "├── SETUP.md" -ForegroundColor Yellow
    Write-Host "├── QUICKSTART.md" -ForegroundColor Yellow
    Write-Host "├── IMPLEMENTATION.md" -ForegroundColor Yellow
    Write-Host "├── run.bat" -ForegroundColor Yellow
    Write-Host "└── run.sh" -ForegroundColor Yellow
}

# Main execution
Clear-Host

# Check Python
if (-not (Test-PythonInstalled)) {
    Write-Host "`nPlease install Python 3.10 or higher from: https://www.python.org/" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Initialize environment
Initialize-VirtualEnv
Activate-VirtualEnv
Setup-Environment

# Install dependencies if not present
if (-not (pip show fastapi -q)) {
    if (-not (Install-Dependencies)) {
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Main menu loop
$continue = $true
while ($continue) {
    Show-Menu
    $choice = Read-Host "Enter your choice (1-6)"
    
    switch ($choice) {
        "1" { 
            Run-CLI
            break
        }
        "2" {
            Run-Server
            break
        }
        "3" {
            Start-Process "http://localhost:8000/docs"
            Write-Host "✓ Opened API documentation in browser" -ForegroundColor Green
            Start-Sleep -Seconds 2
        }
        "4" {
            Install-Dependencies
            Start-Sleep -Seconds 2
        }
        "5" {
            Show-Structure
            Read-Host "`nPress Enter to continue"
        }
        "6" {
            Write-Host "`n👋 Thank you for using OtakuVerse!`n" -ForegroundColor Green
            $continue = $false
        }
        default {
            Write-Host "✗ Invalid choice. Please try again." -ForegroundColor Red
            Start-Sleep -Seconds 2
        }
    }
}
