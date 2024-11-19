# Konomi API Documentation

## API Endpoints

### POST /api/v1/execute
Execute Konomi code and return the results.

#### Request Format
```json
{
    "code": "let x = 42\nask \"What is the meaning of life?\""
}
```

#### Response Format
```json
{
    "success": true,
    "result": "The meaning of life is...",
    "variables": {
        "x": 42
    }
}
```

#### Example Usage
```bash
curl -X POST http://localhost:5000/api/v1/execute \
    -H "Content-Type: application/json" \
    -d '{"code": "let x = 42\nask \"What is x?\""}' 
```

### GET /api/v1/status
Get the current interpreter status.

#### Response Format
```json
{
    "success": true,
    "status": "running",
    "version": "1.0",
    "active_variables": 1
}
```

#### Example Usage
```bash
curl http://localhost:5000/api/v1/status
```

### GET /api/v1/variables
Get all currently defined variables.

#### Response Format
```json
{
    "success": true,
    "variables": {
        "x": 42,
        "name": "Alice"
    }
}
```

#### Example Usage
```bash
curl http://localhost:5000/api/v1/variables
```

## Error Handling
All endpoints return error responses in the following format:

```json
{
    "success": false,
    "error": "Error message description"
}
```

### Common Error Codes
- **400** - Bad Request (invalid input)
- **500** - Internal Server Error

## Authentication
Currently, the API is open and does not require authentication. For production use, it's recommended to implement appropriate authentication mechanisms.
