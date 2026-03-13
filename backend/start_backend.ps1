# ------------------------------
# FarmSyn Global - Start Backend
# ------------------------------

Write-Host "Checking for internet connection..."
$connection = Test-Connection -ComputerName google.com -Count 1 -Quiet
if (-not $connection) {
    Write-Host "No internet connection detected. Please check your connection." -ForegroundColor Red
    exit
}

Write-Host "Internet connection detected..." -ForegroundColor Green

# Define project path (update if necessary)
$projectPath = "C:\Users\congopromotion.store\Documents\backend"

# Move to backend directory
Set-Location $projectPath

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& "$projectPath\venv\Scripts\Activate.ps1"

# Start FastAPI server
