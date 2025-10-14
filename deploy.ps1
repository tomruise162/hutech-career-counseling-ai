# Demo Local Docker Deployment Script (PowerShell)
# Su dung cho Windows

Write-Host "Bat dau Demo Local Docker deployment..." -ForegroundColor Green

# Kiem tra Docker
try {
    $dockerVersion = docker --version 2>&1
    Write-Host "Docker: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "Docker chua duoc cai dat. Vui long cai dat Docker truoc." -ForegroundColor Red
    exit 1
}

# Kiem tra Docker Compose
try {
    $composeVersion = docker-compose --version 2>&1
    Write-Host "Docker Compose: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "Docker Compose chua duoc cai dat. Vui long cai dat Docker Compose truoc." -ForegroundColor Red
    exit 1
}

# Tao file .env neu chua co
if (-not (Test-Path ".env")) {
    Write-Host "Tao file .env..." -ForegroundColor Yellow
    Copy-Item "env.example" ".env"
    Write-Host "Vui long cap nhat OPENAI_API_KEY trong file .env" -ForegroundColor Yellow
}

# Tao thu muc can thiet
Write-Host "Tao thu muc can thiet..." -ForegroundColor Yellow
if (-not (Test-Path "database")) { New-Item -ItemType Directory -Path "database" }
if (-not (Test-Path "ssl")) { New-Item -ItemType Directory -Path "ssl" }

# Build va start containers
Write-Host "Build va start containers..." -ForegroundColor Yellow
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Khoi tao du lieu mau
Write-Host "Khoi tao du lieu mau..." -ForegroundColor Yellow
Start-Sleep -Seconds 10
docker-compose exec backend python init_data.py

# Kiem tra trang thai
Write-Host "Kiem tra trang thai services..." -ForegroundColor Yellow
docker-compose ps

Write-Host "Demo Local deployment hoan tat!" -ForegroundColor Green
Write-Host "Frontend: http://localhost:3001" -ForegroundColor Cyan
Write-Host "Backend API: http://localhost:8001" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8001/docs" -ForegroundColor Cyan
Write-Host "Health Check: http://localhost:8001/health" -ForegroundColor Cyan
Write-Host "Nginx Proxy: http://localhost:8080" -ForegroundColor Cyan
Write-Host ""
Write-Host "HuNext AI Career Counseling da san sang!" -ForegroundColor Magenta
Write-Host ""
Write-Host "Cac lenh huu ich:" -ForegroundColor Yellow
Write-Host "  - Xem logs: docker-compose logs -f" -ForegroundColor White
Write-Host "  - Stop services: docker-compose down" -ForegroundColor White
Write-Host "  - Restart services: docker-compose restart" -ForegroundColor White
Write-Host "  - Update code: docker-compose up -d --build" -ForegroundColor White