# Database Setup Guide

This guide covers setting up the PostgreSQL database for the Passion Detection AI system.

## Prerequisites

- Python 3.8+
- PostgreSQL 12+ (or Docker)
- psycopg2-binary (included in requirements.txt)

## Quick Start

### Option 1: Using Docker (Recommended)

1. **Start PostgreSQL with Docker:**
   ```bash
   docker run --name passion-db \
     -e POSTGRES_DB=passion_detection \
     -e POSTGRES_USER=user \
     -e POSTGRES_PASSWORD=password \
     -p 5432:5432 \
     -d postgres:15
   ```

2. **Run the setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

### Option 2: Local PostgreSQL Installation

1. **Install PostgreSQL:**
   - **macOS:** `brew install postgresql && brew services start postgresql`
   - **Ubuntu/Debian:** `sudo apt-get install postgresql postgresql-contrib`
   - **Windows:** Download from [postgresql.org](https://www.postgresql.org/download/windows/)

2. **Create database and user:**
   ```sql
   CREATE DATABASE passion_detection;
   CREATE USER user WITH PASSWORD 'password';
   GRANT ALL PRIVILEGES ON DATABASE passion_detection TO user;
   ```

3. **Run the setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

## Database Scripts

### 1. Database Setup Script (`database_setup.py`)

Comprehensive database setup with multiple options:

```bash
# Basic setup
python database_setup.py

# Setup with sample data
python database_setup.py --seed

# Test connection only
python database_setup.py --test-only
```

**Features:**
- Creates database if it doesn't exist
- Tests connection
- Creates all tables
- Verifies table creation
- Seeds sample data (optional)

### 2. Database Initialization Script (`init_db.py`)

Simplified initialization for Docker deployments:

```bash
python init_db.py
```

**Features:**
- Waits for database to be available
- Creates all tables
- Creates admin user
- Seeds sample games

### 3. Connection Test Script (`test_db_connection.py`)

Quick connection testing:

```bash
python test_db_connection.py
```

**Features:**
- Tests basic connection
- Tests session creation
- Verifies table existence
- Provides detailed feedback

## Database Schema

The system creates the following tables:

### Core Tables
- **users** - User accounts (parents, admins)
- **children** - Child profiles
- **games** - Available games and activities
- **game_sessions** - Game play sessions and data
- **passion_domains** - Detected passion domains
- **passion_insights** - Specific insights and observations

### Table Relationships
```
users (1) ──── (many) children
children (1) ──── (many) game_sessions
games (1) ──── (many) game_sessions
children (1) ──── (many) passion_domains
passion_domains (1) ──── (many) passion_insights
```

## Configuration

### Environment Variables

Update `backend/.env` with your database settings:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost/passion_detection

# For Docker:
# DATABASE_URL=postgresql://user:password@postgres:5432/passion_detection
```

### Connection Parameters

- **Host:** Database server address
- **Port:** PostgreSQL port (default: 5432)
- **Database:** Database name (default: passion_detection)
- **User:** Database username
- **Password:** Database password

## Database Utilities

The `app/core/db_utils.py` module provides helper functions:

```python
from app.core.db_utils import (
    test_connection,
    get_database_stats,
    create_database_if_not_exists,
    wait_for_database,
    get_table_info,
    backup_database,
    restore_database
)

# Test connection
if test_connection():
    print("Database is accessible")

# Get statistics
stats = get_database_stats()
print(f"Users: {stats.get('users_count', 0)}")

# Wait for database (useful in Docker)
wait_for_database(max_retries=30, delay=2)

# Backup database
backup_database("backups/db_backup.sql")

# Restore database
restore_database("backups/db_backup.sql")
```

## Troubleshooting

### Common Issues

1. **Connection Refused**
   ```
   Error: could not connect to server: Connection refused
   ```
   **Solution:** Ensure PostgreSQL is running and accessible

2. **Authentication Failed**
   ```
   Error: FATAL: password authentication failed
   ```
   **Solution:** Check username/password in DATABASE_URL

3. **Database Does Not Exist**
   ```
   Error: database "passion_detection" does not exist
   ```
   **Solution:** Run `python database_setup.py` to create the database

4. **Permission Denied**
   ```
   Error: permission denied for database
   ```
   **Solution:** Grant proper permissions to the database user

### Debug Commands

```bash
# Test connection manually
psql -h localhost -U user -d passion_detection

# Check PostgreSQL status
brew services list | grep postgresql

# View PostgreSQL logs
tail -f /usr/local/var/log/postgres.log

# Check Docker container
docker logs passion-db
```

## Backup and Recovery

### Creating Backups

```bash
# Manual backup
pg_dump -h localhost -U user -d passion_detection > backup.sql

# Using utility function
python -c "
from app.core.db_utils import backup_database
backup_database('backups/backup_$(date +%Y%m%d_%H%M%S).sql')
"
```

### Restoring Backups

```bash
# Manual restore
psql -h localhost -U user -d passion_detection < backup.sql

# Using utility function
python -c "
from app.core.db_utils import restore_database
restore_database('backups/backup_20231201_120000.sql')
"
```

## Performance Optimization

### Indexes

The system automatically creates indexes for:
- User email (unique)
- Child user_id (foreign key)
- Game sessions child_id and game_id
- Passion domains child_id

### Connection Pooling

SQLAlchemy is configured with connection pooling:
- Pool size: 5-10 connections
- Max overflow: 20 connections
- Pool timeout: 30 seconds

### Monitoring

Use the database utilities to monitor performance:

```python
from app.core.db_utils import get_database_stats

# Get table statistics
stats = get_database_stats()
for table, count in stats.items():
    print(f"{table}: {count} records")
```

## Security Considerations

1. **Use strong passwords** for database users
2. **Limit network access** to database server
3. **Enable SSL** for production deployments
4. **Regular backups** of important data
5. **Monitor access logs** for suspicious activity

## Production Deployment

For production environments:

1. **Use dedicated database server**
2. **Configure SSL connections**
3. **Set up automated backups**
4. **Monitor database performance**
5. **Use connection pooling**
6. **Implement proper access controls**

Example production DATABASE_URL:
```
DATABASE_URL=postgresql://user:strong_password@db.example.com:5432/passion_detection?sslmode=require
``` 