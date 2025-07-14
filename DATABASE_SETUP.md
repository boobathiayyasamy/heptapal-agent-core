# Database Setup Guide for Heptapal Agent Core

This guide explains how to set up the MySQL database for storing reminders and todos in the Heptapal Agent Core application.

## Database Configuration

The application uses MySQL database with the following configuration (stored in `application.yaml`):

```yaml
database:
  connection_name: heptapal-db
  host: 192.168.0.111
  port: 3306
  user: admin
  password: admin
  database: heptapal-db
  charset: utf8mb4
  autocommit: true
  pool_size: 10
  max_overflow: 20
```

## Database Schema

### Reminders Table
- `id`: Primary key, auto-increment
- `title`: Short title for the reminder (VARCHAR(255))
- `description`: Detailed description (TEXT)
- `remind_time`: When to trigger the reminder (DATETIME)
- `created_at`: Creation timestamp (DATETIME)
- `is_active`: Whether the reminder is active (BOOLEAN)

### Todos Table
- `id`: Primary key, auto-increment
- `title`: Short title for the todo (VARCHAR(255))
- `description`: Detailed description (TEXT, optional)
- `priority`: Priority level - low, medium, high (ENUM)
- `status`: Current status - pending, in_progress, completed (ENUM)
- `due_date`: Optional due date (DATE)
- `created_at`: Creation timestamp (DATETIME)
- `completed_at`: Completion timestamp (DATETIME, optional)

## Setup Instructions

### 1. Install Dependencies

Since this is a uv project, add the required dependencies:

```bash
uv add mysql-connector-python sqlalchemy
```

The `pyyaml` dependency is already included in the project.

### 2. Create Database

Connect to your MySQL server and run the schema script:

```bash
mysql -h 192.168.0.111 -u admin -p < database_schema.sql
```

Or manually create the database:

```sql
CREATE DATABASE IF NOT EXISTS `heptapal-db` 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
```

### 3. Initialize Database Tables

Run the database initialization script:

```bash
python -m db.init_db
```

This will:
- Connect to the database using the configuration in `application.yaml`
- Create all necessary tables
- Test the connection
- Verify table creation

### 4. Verify Setup

You can verify the setup by checking the database:

```sql
USE heptapal-db;
SHOW TABLES;
DESCRIBE reminders;
DESCRIBE todos;
```

## Architecture Overview

The database implementation follows the Single Responsibility Principle:

### 1. Database Connection (`db/connection.py`)
- **Responsibility**: Handle database connections and session management
- **Features**: Connection pooling, error handling, connection testing

### 2. Database Models (`db/models.py`)
- **Responsibility**: Define database table structures and relationships
- **Features**: SQLAlchemy ORM models, data validation, serialization

### 3. Database Repositories (`db/repositories.py`)
- **Responsibility**: Handle database operations for reminders and todos
- **Features**: CRUD operations, search functionality, statistics

### 4. Tool Integration
- **ReminderTools**: Uses `ReminderRepository` for database operations
- **TodoTools**: Uses `TodoRepository` for database operations

## Usage Examples

### Adding a Reminder
```python
from root_agent.sub_agents.reminder_agent.tools.reminder_tools import ReminderTools

# Initialize with config
config = {"database": {...}}  # Your database config
reminder_tools = ReminderTools(config)

# Add a reminder
result = reminder_tools.add_reminder(
    title="Meeting",
    description="Team standup meeting",
    remind_time="tomorrow at 9 AM"
)
```

### Adding a Todo
```python
from root_agent.sub_agents.todo_agent.tools.todo_tools import TodoTools

# Initialize with config
config = {"database": {...}}  # Your database config
todo_tools = TodoTools(config)

# Add a todo
result = todo_tools.add_todo(
    title="Complete Documentation",
    description="Write API documentation",
    priority="high",
    due_date="2024-12-20"
)
```

## Troubleshooting

### Connection Issues
1. Verify MySQL server is running on the specified host and port
2. Check that the user has proper permissions
3. Ensure the database exists
4. Verify network connectivity

### Table Creation Issues
1. Check that the user has CREATE TABLE permissions
2. Verify the database exists and is accessible
3. Check for any existing tables with conflicting names

### Performance Issues
1. Monitor connection pool usage
2. Check database indexes are being used
3. Consider adjusting pool_size and max_overflow settings

## Security Considerations

1. **Credentials**: Store database credentials securely, consider using environment variables
2. **Network**: Ensure database is not exposed to public networks
3. **Permissions**: Use minimal required permissions for the database user
4. **Encryption**: Consider enabling SSL/TLS for database connections

## Backup and Recovery

Regular backups are recommended:

```bash
# Create backup
mysqldump -h 192.168.0.111 -u admin -p heptapal-db > backup.sql

# Restore backup
mysql -h 192.168.0.111 -u admin -p heptapal-db < backup.sql
```

## Monitoring

Monitor database performance and health:

```sql
-- Check table sizes
SELECT 
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.tables 
WHERE table_schema = 'heptapal-db';

-- Check active connections
SHOW PROCESSLIST;
``` 