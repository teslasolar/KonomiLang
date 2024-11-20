# Core API Endpoints Documentation

## Authentication
All API endpoints require authentication using Bearer token in the Authorization header:
```
Authorization: Bearer <your_token>
```

## Rate Limits
- Default rate limit: 100 requests per minute
- Enhanced rate limit (authenticated users): 1000 requests per minute
- Burst limit: 10 requests per second

## Common Error Responses
```json
{
    "success": false,
    "error": {
        "code": "ERROR_CODE",
        "message": "Human readable error message"
    }
}
```

## Core Endpoints

### Execute Konomi Code
```
POST /api/v1/execute
```

Request format:
```json
{
    "code": "string",
    "timeout": "optional number (seconds)"
}
```

Response format:
```json
{
    "success": true,
    "result": {
        "output": "string",
        "execution_time": "number"
    }
}
```

### Get Interpreter Status
```
GET /api/v1/status
```

Response format:
```json
{
    "success": true,
    "status": {
        "version": "string",
        "uptime": "number",
        "active_sessions": "number"
    }
}
```

### Get Variables
```
GET /api/v1/variables
```

Response format:
```json
{
    "success": true,
    "variables": {
        "variable_name": {
            "type": "string",
            "value": "any"
        }
    }
}
```
