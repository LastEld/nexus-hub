# NexusHub Setup Script for Windows
# This script sets up the development environment

Write-Host "🚀 NexusHub Setup Script" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check if Docker Compose is available
if (!(Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker Compose is not installed. Please install Docker Compose first." -ForegroundColor Red
    exit 1
}

# Create environment files if they don't exist
if (!(Test-Path "backend\.env")) {
    Write-Host "📝 Creating backend .env file..." -ForegroundColor Yellow
    Copy-Item "backend\.env.example" "backend\.env"
    Write-Host "✅ Backend .env created. Please edit it with your configuration." -ForegroundColor Green
}

if (!(Test-Path "frontend\.env.local")) {
    Write-Host "📝 Creating frontend .env.local file..." -ForegroundColor Yellow
    Copy-Item "frontend\.env.example" "frontend\.env.local"
    Write-Host "✅ Frontend .env.local created." -ForegroundColor Green
}

# Start Docker services
Write-Host ""
Write-Host "🐳 Starting Docker services..." -ForegroundColor Cyan
docker-compose up -d

# Wait for PostgreSQL to be ready
Write-Host ""
Write-Host "⏳ Waiting for PostgreSQL to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Run database migrations
Write-Host ""
Write-Host "📊 Running database migrations..." -ForegroundColor Cyan
docker-compose exec -T backend alembic upgrade head

# Create admin user
Write-Host ""
Write-Host "👤 Creating admin user..." -ForegroundColor Cyan
Write-Host "Please enter admin user details:" -ForegroundColor Yellow
docker-compose exec backend python scripts/create_admin.py

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Access points:" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost:3000"
Write-Host "   Backend API: http://localhost:8000"
Write-Host "   API Docs: http://localhost:8000/api/v1/docs"
Write-Host "   Adminer: http://localhost:8080"
Write-Host ""
Write-Host "🎉 Happy coding!" -ForegroundColor Magenta
