# GameMind AI - Windows launcher
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    Write-Host "Python não foi encontrado. Instale Python 3.10+ e marque Add Python to PATH." -ForegroundColor Yellow
    exit 1
}

Write-Host "Treinando GameMind AI por 3000 partidas..." -ForegroundColor Cyan
py train.py --episodes 3000
if ($LASTEXITCODE -ne 0) { throw "O treinamento falhou." }

Write-Host "Agora a IA vai jogar usando a memória salva..." -ForegroundColor Green
py play.py
