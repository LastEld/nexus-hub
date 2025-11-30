#!/bin/bash

# NexusHub Setup Script
# This script sets up the development environment

set -e

echo "🚀 NexusHub Setup Script"
echo "========================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create environment files if they don't exist
if [ ! -f backend/.env ]; then
    echo "📝 Creating backend .env file..."
    cp backend/.env.example backend/.env
    echo "✅ Backend .env created. Please edit it with your configuration."
fi

if [ ! -f frontend/.env.local ]; then
    echo "📝 Creating frontend .env.local file..."
    cp frontend/.env.example frontend/.env.local
    echo "✅ Frontend .env.local created."
fi

# Start Docker services
echo ""
echo "🐳 Starting Docker services..."
docker-compose up -d

# Wait for PostgreSQL to be ready
echo ""
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 5

# Run database migrations
echo ""
echo "📊 Running database migrations..."
docker-compose exec -T backend alembic upgrade head

# Create admin user
echo ""
echo "👤 Creating admin user..."
echo "Please enter admin user details:"
docker-compose exec backend python scripts/create_admin.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "📍 Access points:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/api/v1/docs"
echo "   Adminer: http://localhost:8080"
echo ""
echo "🎉 Happy coding!"
