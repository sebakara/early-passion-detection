#!/bin/bash

echo "🚀 Setting up Passion Detection AI System..."

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p backend/uploads
mkdir -p backend/ml_models
mkdir -p frontend/public

# Backend setup
echo "🐍 Setting up Python backend..."
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with secure credentials
cat > .env << EOF
# Application Settings
APP_NAME=Passion Detection AI
DEBUG=True
SECRET_KEY=passion-detection-ai-secret-key-2024-change-in-production

# Database Configuration
DATABASE_URL=postgresql://postgres:mavin12345@localhost/kidedutech

# Security
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_HOSTS=["http://localhost:3000", "http://localhost:3001"]

# ML Models
MODEL_PATH=ml_models/
MODEL_VERSION=v1.0

# File Upload
UPLOAD_DIR=uploads/
MAX_FILE_SIZE=10485760

# Logging
LOG_LEVEL=INFO

# Child Safety
MIN_AGE=3
MAX_AGE=12
PARENTAL_CONSENT_REQUIRED=True
DATA_RETENTION_DAYS=2555
EOF

# Test database connection and setup
echo "Testing database connection..."
python test_db_connection.py

if [ $? -eq 0 ]; then
    echo "✅ Database connection successful"
    echo "Initializing database..."
    python init_db.py
else
    echo "⚠️  Database connection failed. Please ensure PostgreSQL is running."
    echo "You can start PostgreSQL with: brew services start postgresql"
    echo "Or use Docker: docker run --name postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=passion_detection -p 5432:5432 -d postgres:15"
fi

cd ..

# Frontend setup
echo "⚛️ Setting up React frontend..."
cd frontend

# Install dependencies
npm install

cd ..

echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Configure your database in backend/.env"
echo "2. Start the backend: cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "3. Start the frontend: cd frontend && npm start"
echo ""
echo "🌐 The application will be available at:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs" 