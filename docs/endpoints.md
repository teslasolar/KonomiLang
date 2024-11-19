# Konomi API Endpoints

## REST API Reference

This document provides detailed information about all available API endpoints in the Konomi language implementation.

## Base URL
All API endpoints are relative to: `http://localhost:5000/api/v1/`

## Available Endpoints

### Execute Code
- **Endpoint**: `/execute`
- **Method**: POST
- **Description**: Execute Konomi code and return the results
- **Content-Type**: application/json

#### Request Body
```json
{
    "code": "string"  // Required: Konomi code to execute
}
```

#### Success Response (200 OK)
```json
{
    "success": true,
    "result": "string",  // Execution result
    "variables": {       // Current state of variables
        "key": "value"
    }
}
```

#### Error Response (400 Bad Request)
```json
{
    "success": false,
    "error": "Error description"
}
```

### Get Status
- **Endpoint**: `/status`
- **Method**: GET
- **Description**: Get current interpreter status and version

#### Success Response (200 OK)
```json
{
    "success": true,
    "status": "running",
    "version": "1.0",
    "active_variables": 1
}
```

### Get Variables
- **Endpoint**: `/variables`
- **Method**: GET
- **Description**: Get all currently defined variables

#### Success Response (200 OK)
```json
{
    "success": true,
    "variables": {
        "variable_name": "value"
    }
}
```

## Error Handling

### Common HTTP Status Codes
- `200 OK`: Request successful
- `400 Bad Request`: Invalid input or request
- `500 Internal Server Error`: Server-side error

### Error Response Format
All error responses follow this format:
```json
{
    "success": false,
    "error": "Detailed error message"
}
```

## Security Considerations
- The API currently does not require authentication
- Rate limiting is not implemented
- Consider implementing authentication for production use
