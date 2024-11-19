# Konomi Database Grid Documentation

## Overview

The Konomi database grid is organized as a 5x5 matrix of SQLite databases, each dedicated to storing specific aspects of the language implementation. The grid is structured into five distinct rows (A-E), with each row focusing on a particular domain of functionality.

## Grid Structure

```
db_grid/
├── Row A: Core Language Features
│   ├── A1: Lexer tokens and patterns
│   ├── A2: Parser rules and AST structures
│   ├── A3: Interpreter states
│   ├── A4: Symbol table and scope management
│   └── A5: Type system definitions
├── Row B: AI Integration
│   ├── B1: OpenAI API calls history
│   ├── B2: Model configurations
│   ├── B3: Prompt templates
│   ├── B4: Response caching
│   └── B5: AI context management
├── Row C: REPL and Interface
│   ├── C1: Command history
│   ├── C2: User sessions
│   ├── C3: Completion suggestions
│   ├── C4: Error logs
│   └── C5: Interface preferences
├── Row D: File System Operations
│   ├── D1: File operation logs
│   ├── D2: Directory structure cache
│   ├── D3: File metadata
│   ├── D4: Access permissions
│   └── D5: File operation queue
└── Row E: System Management
    ├── E1: Performance metrics
    ├── E2: User settings
    ├── E3: System configurations
    ├── E4: Backup metadata
    └── E5: Audit logs
```

## Database Purposes and Schemas

### Row A: Core Language Features

#### A1: Lexer Tokens and Patterns
Purpose: Stores lexical analysis patterns and token definitions
```sql
CREATE TABLE tokens (
    id INTEGER PRIMARY KEY,
    token_type TEXT NOT NULL,
    pattern TEXT NOT NULL,
    priority INTEGER NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE token_matches (
    id INTEGER PRIMARY KEY,
    token_id INTEGER,
    source_text TEXT NOT NULL,
    line_number INTEGER,
    column_number INTEGER,
    matched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (token_id) REFERENCES tokens(id)
);
```

#### A2: Parser Rules and AST Structures
Purpose: Maintains parser grammar rules and AST node definitions
```sql
CREATE TABLE parser_rules (
    id INTEGER PRIMARY KEY,
    rule_name TEXT NOT NULL,
    production TEXT NOT NULL,
    precedence INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ast_nodes (
    id INTEGER PRIMARY KEY,
    node_type TEXT NOT NULL,
    parent_id INTEGER,
    source_location TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES ast_nodes(id)
);
```

#### A3: Interpreter States
Purpose: Tracks interpreter execution states and contexts
```sql
CREATE TABLE interpreter_states (
    id INTEGER PRIMARY KEY,
    state_type TEXT NOT NULL,
    context_data TEXT,
    parent_state_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_state_id) REFERENCES interpreter_states(id)
);
```

#### A4: Symbol Table and Scope Management
Purpose: Manages variable scopes and symbol resolution
```sql
CREATE TABLE symbols (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    scope_id INTEGER,
    value TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE scopes (
    id INTEGER PRIMARY KEY,
    scope_type TEXT NOT NULL,
    parent_scope_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_scope_id) REFERENCES scopes(id)
);
```

#### A5: Type System Definitions
Purpose: Stores type definitions and relationships
```sql
CREATE TABLE types (
    id INTEGER PRIMARY KEY,
    type_name TEXT NOT NULL,
    parent_type_id INTEGER,
    properties TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_type_id) REFERENCES types(id)
);
```

### Row B: AI Integration

#### B1: OpenAI API Calls History
Purpose: Logs API interactions with OpenAI
```sql
CREATE TABLE api_calls (
    id INTEGER PRIMARY KEY,
    endpoint TEXT NOT NULL,
    request_data TEXT,
    response_data TEXT,
    tokens_used INTEGER,
    cost REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### B2: Model Configurations
Purpose: Stores AI model configurations
```sql
CREATE TABLE model_configs (
    id INTEGER PRIMARY KEY,
    model_name TEXT NOT NULL,
    parameters TEXT,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### B3: Prompt Templates
Purpose: Manages reusable prompt templates
```sql
CREATE TABLE prompt_templates (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    template TEXT NOT NULL,
    variables TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### B4: Response Caching
Purpose: Caches AI responses for performance
```sql
CREATE TABLE response_cache (
    id INTEGER PRIMARY KEY,
    prompt_hash TEXT UNIQUE NOT NULL,
    response TEXT,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### B5: AI Context Management
Purpose: Manages conversation contexts
```sql
CREATE TABLE contexts (
    id INTEGER PRIMARY KEY,
    context_type TEXT NOT NULL,
    content TEXT,
    max_tokens INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Row C: REPL and Interface

#### C1: Command History
Purpose: Stores user command history
```sql
CREATE TABLE commands (
    id INTEGER PRIMARY KEY,
    session_id TEXT NOT NULL,
    command TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### C2: User Sessions
Purpose: Manages REPL sessions
```sql
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY,
    user_id TEXT,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP,
    status TEXT
);
```

#### C3: Completion Suggestions
Purpose: Stores autocompletion data
```sql
CREATE TABLE completions (
    id INTEGER PRIMARY KEY,
    trigger TEXT NOT NULL,
    suggestion TEXT NOT NULL,
    context TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### C4: Error Logs
Purpose: Records REPL errors
```sql
CREATE TABLE error_logs (
    id INTEGER PRIMARY KEY,
    error_type TEXT NOT NULL,
    message TEXT,
    stack_trace TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### C5: Interface Preferences
Purpose: Stores user interface settings
```sql
CREATE TABLE preferences (
    id INTEGER PRIMARY KEY,
    user_id TEXT,
    setting_key TEXT NOT NULL,
    setting_value TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Row D: File System Operations

#### D1: File Operation Logs
Purpose: Tracks file system operations
```sql
CREATE TABLE file_operations (
    id INTEGER PRIMARY KEY,
    operation_type TEXT NOT NULL,
    file_path TEXT NOT NULL,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### D2: Directory Structure Cache
Purpose: Caches directory structure
```sql
CREATE TABLE directory_cache (
    id INTEGER PRIMARY KEY,
    path TEXT NOT NULL,
    parent_path TEXT,
    is_directory BOOLEAN,
    last_modified TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### D3: File Metadata
Purpose: Stores file metadata
```sql
CREATE TABLE file_metadata (
    id INTEGER PRIMARY KEY,
    file_path TEXT NOT NULL,
    size INTEGER,
    mime_type TEXT,
    hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### D4: Access Permissions
Purpose: Manages file permissions
```sql
CREATE TABLE permissions (
    id INTEGER PRIMARY KEY,
    file_path TEXT NOT NULL,
    user_id TEXT,
    access_level TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### D5: File Operation Queue
Purpose: Manages pending file operations
```sql
CREATE TABLE operation_queue (
    id INTEGER PRIMARY KEY,
    operation_type TEXT NOT NULL,
    parameters TEXT,
    priority INTEGER,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Row E: System Management

#### E1: Performance Metrics
Purpose: Records system performance data
```sql
CREATE TABLE metrics (
    id INTEGER PRIMARY KEY,
    metric_type TEXT NOT NULL,
    value REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### E2: User Settings
Purpose: Stores user preferences
```sql
CREATE TABLE user_settings (
    id INTEGER PRIMARY KEY,
    user_id TEXT NOT NULL,
    setting_key TEXT NOT NULL,
    setting_value TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### E3: System Configurations
Purpose: Manages system settings
```sql
CREATE TABLE system_configs (
    id INTEGER PRIMARY KEY,
    config_key TEXT NOT NULL,
    config_value TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### E4: Backup Metadata
Purpose: Tracks backup information
```sql
CREATE TABLE backups (
    id INTEGER PRIMARY KEY,
    backup_path TEXT NOT NULL,
    size INTEGER,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### E5: Audit Logs
Purpose: Records system audit trail
```sql
CREATE TABLE audit_logs (
    id INTEGER PRIMARY KEY,
    event_type TEXT NOT NULL,
    user_id TEXT,
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Usage Examples

### Example 1: Tracking Lexer Tokens
```sql
-- Insert a new token pattern
INSERT INTO db_grid/A1/database.db:tokens (token_type, pattern, priority, description)
VALUES ('IDENTIFIER', '[a-zA-Z_][a-zA-Z0-9_]*', 1, 'Variable or function identifier');

-- Query matched tokens
SELECT * FROM db_grid/A1/database.db:token_matches 
WHERE token_id IN (SELECT id FROM tokens WHERE token_type = 'IDENTIFIER')
ORDER BY matched_at DESC LIMIT 5;
```

### Example 2: Managing API Calls
```sql
-- Log an API call
INSERT INTO db_grid/B1/database.db:api_calls (endpoint, request_data, response_data, tokens_used, cost)
VALUES (
    '/v1/completions',
    '{"prompt": "Hello, world!", "max_tokens": 50}',
    '{"text": "Hi there!", "usage": {"total_tokens": 10}}',
    10,
    0.002
);

-- Get API usage statistics
SELECT 
    DATE(created_at) as date,
    COUNT(*) as calls,
    SUM(tokens_used) as total_tokens,
    SUM(cost) as total_cost
FROM db_grid/B1/database.db:api_calls
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

### Example 3: REPL Session Management
```sql
-- Start a new session
INSERT INTO db_grid/C2/database.db:sessions (user_id, status)
VALUES ('user123', 'active');

-- Record command history
INSERT INTO db_grid/C1/database.db:commands (session_id, command)
VALUES (
    (SELECT id FROM db_grid/C2/database.db:sessions WHERE user_id = 'user123' ORDER BY start_time DESC LIMIT 1),
    'print("Hello, World!")'
);
```

### Example 4: File Operations
```sql
-- Log a file operation
INSERT INTO db_grid/D1/database.db:file_operations (operation_type, file_path, status)
VALUES ('CREATE', '/workspace/main.py', 'SUCCESS');

-- Check file permissions
SELECT * FROM db_grid/D4/database.db:permissions
WHERE file_path = '/workspace/main.py'
AND user_id = 'user123';
```

### Example 5: System Monitoring
```sql
-- Record performance metric
INSERT INTO db_grid/E1/database.db:metrics (metric_type, value)
VALUES ('memory_usage', 256.5);

-- Get system configuration
SELECT config_value FROM db_grid/E3/database.db:system_configs
WHERE config_key = 'max_memory_limit';
```

## Maintenance and Backup

Each database in the grid should be backed up regularly. The backup metadata is stored in the E4 database, which tracks all backup operations and their status.

To maintain optimal performance:
1. Regularly clean up old entries from cache tables (B4, D2)
2. Archive old logs (C4, D1, E5)
3. Monitor database sizes and performance metrics (E1)
4. Maintain indexes on frequently queried columns

## Security Considerations

1. All sensitive data in the databases should be encrypted
2. Access to the databases should be controlled through the permissions system (D4)
3. All operations should be logged in the audit system (E5)
4. Regular security audits should be performed using the logs
