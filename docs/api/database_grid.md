# Database Grid API Documentation

## Connection Management

### Initialize Connection Pool
```
POST /api/v1/database/init
```

Request format:
```json
{
    "max_connections": "number",
    "timeout": "number"
}
```

Response format:
```json
{
    "success": true,
    "pool_status": {
        "active_connections": "number",
        "available_connections": "number"
    }
}
```

## Database Operations

### Execute Query
```
POST /api/v1/database/execute
```

Request format:
```json
{
    "grid_id": "string (A1-G5)",
    "query": "string",
    "parameters": "array (optional)"
}
```

Response format:
```json
{
    "success": true,
    "results": {
        "rows": "array",
        "affected_rows": "number"
    }
}
```

## Monitoring Endpoints

### Get Database Status
```
GET /api/v1/database/status/:grid_id
```

Response format:
```json
{
    "success": true,
    "status": {
        "size": "number (MB)",
        "tables": "number",
        "total_records": "number",
        "health": "string"
    }
}
```

### Get Performance Metrics
```
GET /api/v1/database/metrics/:grid_id
```

Response format:
```json
{
    "success": true,
    "metrics": {
        "query_time_avg": "number",
        "connections_active": "number",
        "memory_usage": "number"
    }
}
```

## Backup/Restore Operations

### Create Backup
```
POST /api/v1/database/backup/:grid_id
```

Request format:
```json
{
    "backup_type": "full|incremental",
    "compression": "boolean"
}
```

Response format:
```json
{
    "success": true,
    "backup": {
        "id": "string",
        "timestamp": "string",
        "size": "number",
        "type": "string"
    }
}
```

### Restore Database
```
POST /api/v1/database/restore/:grid_id
```

Request format:
```json
{
    "backup_id": "string",
    "validate": "boolean"
}
```

Response format:
```json
{
    "success": true,
    "restore": {
        "timestamp": "string",
        "tables_restored": "number",
        "records_restored": "number"
    }
}
```
