import os
import sqlite3

def initialize_database(db_path, schema_queries):
    """Initialize a single database with its schema."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        for query in schema_queries:
            cursor.execute(query)
        
        conn.commit()
        conn.close()
        print(f"Successfully initialized {db_path}")
        return True
    except Exception as e:
        print(f"Error initializing {db_path}: {str(e)}")
        return False

# Schema definitions for each database
SCHEMAS = {
    'A1': [
        '''CREATE TABLE IF NOT EXISTS tokens (
            id INTEGER PRIMARY KEY,
            token_type TEXT NOT NULL,
            pattern TEXT NOT NULL,
            priority INTEGER NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''',
        '''CREATE TABLE IF NOT EXISTS token_matches (
            id INTEGER PRIMARY KEY,
            token_id INTEGER,
            source_text TEXT NOT NULL,
            line_number INTEGER,
            column_number INTEGER,
            matched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (token_id) REFERENCES tokens(id)
        )'''
    ],
    'A2': [
        '''CREATE TABLE IF NOT EXISTS parser_rules (
            id INTEGER PRIMARY KEY,
            rule_name TEXT NOT NULL,
            production TEXT NOT NULL,
            precedence INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''',
        '''CREATE TABLE IF NOT EXISTS ast_nodes (
            id INTEGER PRIMARY KEY,
            node_type TEXT NOT NULL,
            parent_id INTEGER,
            source_location TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_id) REFERENCES ast_nodes(id)
        )'''
    ],
    'A3': [
        '''CREATE TABLE IF NOT EXISTS interpreter_states (
            id INTEGER PRIMARY KEY,
            state_type TEXT NOT NULL,
            context_data TEXT,
            parent_state_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_state_id) REFERENCES interpreter_states(id)
        )'''
    ],
    'A4': [
        '''CREATE TABLE IF NOT EXISTS symbols (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            scope_id INTEGER,
            value TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''',
        '''CREATE TABLE IF NOT EXISTS scopes (
            id INTEGER PRIMARY KEY,
            scope_type TEXT NOT NULL,
            parent_scope_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_scope_id) REFERENCES scopes(id)
        )'''
    ],
    'A5': [
        '''CREATE TABLE IF NOT EXISTS types (
            id INTEGER PRIMARY KEY,
            type_name TEXT NOT NULL,
            parent_type_id INTEGER,
            properties TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_type_id) REFERENCES types(id)
        )'''
    ],
    'B1': [
        '''CREATE TABLE IF NOT EXISTS api_calls (
            id INTEGER PRIMARY KEY,
            endpoint TEXT NOT NULL,
            request_data TEXT,
            response_data TEXT,
            tokens_used INTEGER,
            cost REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
    ],
    'B2': [
        '''CREATE TABLE IF NOT EXISTS model_configs (
            id INTEGER PRIMARY KEY,
            model_name TEXT NOT NULL,
            parameters TEXT,
            active BOOLEAN DEFAULT true,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
    ],
    'B3': [
        '''CREATE TABLE IF NOT EXISTS prompt_templates (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            template TEXT NOT NULL,
            variables TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
    ],
    'B4': [
        '''CREATE TABLE IF NOT EXISTS response_cache (
            id INTEGER PRIMARY KEY,
            prompt_hash TEXT UNIQUE NOT NULL,
            response TEXT,
            expires_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
    ],
    'B5': [
        '''CREATE TABLE IF NOT EXISTS contexts (
            id INTEGER PRIMARY KEY,
            context_type TEXT NOT NULL,
            content TEXT,
            max_tokens INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
    ],
    'C1': [
        '''CREATE TABLE IF NOT EXISTS commands (
            id INTEGER PRIMARY KEY,
            session_id TEXT NOT NULL,
            command TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
    ],
    'C2': [
        '''CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP,
            status TEXT
        )'''
    ],
    'C3': [
        '''CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY,
            trigger TEXT NOT NULL,
            suggestion TEXT NOT NULL,
            context TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
    ],
    'C4': [
        '''CREATE TABLE IF NOT EXISTS error_logs (
            id INTEGER PRIMARY KEY,
            error_type TEXT NOT NULL,
            message TEXT,
            stack_trace TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
    ],
    'C5': [
        '''CREATE TABLE IF NOT EXISTS preferences (
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            setting_key TEXT NOT NULL,
            setting_value TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
    ],
    'D1': [
        '''CREATE TABLE IF NOT EXISTS file_operations (
            id INTEGER PRIMARY KEY,
            operation_type TEXT NOT NULL,
            file_path TEXT NOT NULL,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
    ],
    'D2': [
        '''CREATE TABLE IF NOT EXISTS directory_cache (
            id INTEGER PRIMARY KEY,
            path TEXT NOT NULL,
            parent_path TEXT,
            is_directory BOOLEAN,
            last_modified TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
    ],
    'D3': [
        '''CREATE TABLE IF NOT EXISTS file_metadata (
            id INTEGER PRIMARY KEY,
            file_path TEXT NOT NULL,
            size INTEGER,
            mime_type TEXT,
            hash TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
    ],
    'D4': [
        '''CREATE TABLE IF NOT EXISTS permissions (
            id INTEGER PRIMARY KEY,
            file_path TEXT NOT NULL,
            user_id TEXT,
            access_level TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
    ],
    'D5': [
        '''CREATE TABLE IF NOT EXISTS operation_queue (
            id INTEGER PRIMARY KEY,
            operation_type TEXT NOT NULL,
            parameters TEXT,
            priority INTEGER,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
    ],
    'E1': [
        '''CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY,
            metric_type TEXT NOT NULL,
            value REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
    ],
    'E2': [
        '''CREATE TABLE IF NOT EXISTS user_settings (
            id INTEGER PRIMARY KEY,
            user_id TEXT NOT NULL,
            setting_key TEXT NOT NULL,
            setting_value TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
    ],
    'E3': [
        '''CREATE TABLE IF NOT EXISTS system_configs (
            id INTEGER PRIMARY KEY,
            config_key TEXT NOT NULL,
            config_value TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
    ],
    'E4': [
        '''CREATE TABLE IF NOT EXISTS backups (
            id INTEGER PRIMARY KEY,
            backup_path TEXT NOT NULL,
            size INTEGER,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
    ],
    'E5': [
        '''CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY,
            event_type TEXT NOT NULL,
            user_id TEXT,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
    ]
}

def main():
    base_dir = "db_grid"
    success_count = 0
    total_dbs = 25

    # Initialize each database
    for row in 'ABCDE':
        for col in range(1, 6):
            position = f"{row}{col}"
            db_path = os.path.join(base_dir, position, "database.db")
            
            if position in SCHEMAS:
                if initialize_database(db_path, SCHEMAS[position]):
                    success_count += 1
            else:
                print(f"Error: No schema defined for database {position}")

    print(f"\nInitialization complete:")
    print(f"Successfully initialized {success_count}/{total_dbs} databases")
    return success_count == total_dbs

if __name__ == "__main__":
    if main():
        print("Success: All databases initialized successfully!")
        exit(0)
    else:
        print("Error: Some databases were not initialized properly.")
        exit(1)
