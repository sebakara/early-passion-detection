#!/bin/bash

echo "🗄️  Setting up PostgreSQL database for Passion Detection AI..."

# Database credentials
DB_USER="postgres"
DB_PASSWORD="mavin12345"
DB_NAME="kidedutech"

echo "Creating database user: $DB_USER"
echo "Database name: $DB_NAME"

# Create database user
psql postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" 2>/dev/null || echo "User $DB_USER already exists or error occurred"

# Create database
echo "Creating database: $DB_NAME"
psql postgres -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;" 2>/dev/null || echo "Database $DB_NAME already exists or error occurred"

# Grant privileges
echo "Granting privileges..."
psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" 2>/dev/null || echo "Privileges already granted or error occurred"

echo "✅ Database setup completed!"
echo ""
echo "Database credentials:"
echo "  User: $DB_USER"
echo "  Password: $DB_PASSWORD"
echo "  Database: $DB_NAME"
echo "  Host: localhost"
echo "  Port: 5432"
echo ""
echo "You can now run: ./setup.sh" 