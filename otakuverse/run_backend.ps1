# OtakuVerse Backend Launcher
# Sets PYTHONPATH to include user site-packages before running uvicorn

$pythonUserSite = "C:\Users\Shriyansh Mishra\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages"
$pythonExe = "C:\Users\Shriyansh Mishra\AppData\Local\Microsoft\WindowsApps\python.exe"

# Set environment
$env:PYTHONPATH = $pythonUserSite + ";$env:PYTHONPATH"
$env:PYTHONUSERBASE = "C:\Users\Shriyansh Mishra\AppData\Roaming\Python"

# Load .env file
$envFile = ".env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        $line = $_
        if ($line -and -not $line.StartsWith("#")) {
            $parts = $line -split "=", 2
            if ($parts.Length -eq 2) {
                $key = $parts[0].Trim().Trim('"')
                $value = $parts[1].Trim().Trim('"')
                [Environment]::SetEnvironmentVariable($key, $value)
                Write-Host "Loaded: $key" -ForegroundColor Cyan
            }
        }
    }
}

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║       🎌 OtakuVerse Backend Server - Starting 🎌          ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$port = [Environment]::GetEnvironmentVariable("API_PORT") ?? "8002"
Write-Host "📍 Backend URL: http://localhost:$port" -ForegroundColor Green
Write-Host "📚 API Docs: http://localhost:$port/docs" -ForegroundColor Green
Write-Host "📖 ReDoc: http://localhost:$port/redoc" -ForegroundColor Green
Write-Host ""

# Start backend without reload to avoid subprocess issues
& $pythonExe -m uvicorn api.server_real_data:app --host 0.0.0.0 --port $port
