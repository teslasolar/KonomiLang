# API Documentation

Complete API reference for the Konomi Language

## API Endpoints


### GET /static/<path:filename>









### GET /api/v1/monitor/status

Get overall grid status.









### GET /api/v1/monitor/database/<position>

Get status for a specific database.









### GET /api/v1/monitor/metrics

Get performance metrics for all databases.









### POST /api/v1/monitor/check

Manually trigger a monitoring check.









### GET /api/v1/monitor/backups

List all available backups.









### POST /api/v1/monitor/backups

Create a new backup.









### POST /api/v1/monitor/backups/restore

Restore from a backup.









### GET /docs/

Render main documentation page.









### GET /docs/api

Render API documentation page.









### GET /docs/syntax

Render syntax documentation page.









### GET /docs/endpoints

Render endpoints documentation page.









### GET /

Render main page with REPL interface.









### GET /examples

Render examples page.









### GET /generation

Render code generation page.









### POST /execute

Execute Konomi code from web interface.









### POST /api/v1/execute

Execute Konomi code via API.









### GET /api/v1/status

Get interpreter status.









### GET /api/v1/variables

Get all defined variables.










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