"""
Database Schema Definitions
"""

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
        );''',
        '''CREATE TABLE IF NOT EXISTS token_matches (
            id INTEGER PRIMARY KEY,
            token_id INTEGER,
            source_text TEXT NOT NULL,
            line_number INTEGER,
            column_number INTEGER,
            matched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (token_id) REFERENCES tokens(id)
        );'''
    ],
    'A2': [
        '''CREATE TABLE IF NOT EXISTS parser_rules (
            id INTEGER PRIMARY KEY,
            rule_name TEXT NOT NULL,
            production TEXT NOT NULL,
            precedence INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );''',
        '''CREATE TABLE IF NOT EXISTS ast_nodes (
            id INTEGER PRIMARY KEY,
            node_type TEXT NOT NULL,
            parent_id INTEGER,
            source_location TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_id) REFERENCES ast_nodes(id)
        );'''
    ],
    'A3': [
        '''CREATE TABLE IF NOT EXISTS interpreter_states (
            id INTEGER PRIMARY KEY,
            state_type TEXT NOT NULL,
            context_data TEXT,
            parent_state_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_state_id) REFERENCES interpreter_states(id)
        );'''
    ],
    'A4': [
        '''CREATE TABLE IF NOT EXISTS symbols (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            scope_id INTEGER,
            value TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );''',
        '''CREATE TABLE IF NOT EXISTS scopes (
            id INTEGER PRIMARY KEY,
            scope_type TEXT NOT NULL,
            parent_scope_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_scope_id) REFERENCES scopes(id)
        );'''
    ],
    'A5': [
        '''CREATE TABLE IF NOT EXISTS types (
            id INTEGER PRIMARY KEY,
            type_name TEXT NOT NULL,
            parent_type_id INTEGER,
            properties TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_type_id) REFERENCES types(id)
        );'''
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
        );'''
    ],
    'B2': [
        '''CREATE TABLE IF NOT EXISTS model_configs (
            id INTEGER PRIMARY KEY,
            model_name TEXT NOT NULL,
            parameters TEXT,
            active BOOLEAN DEFAULT true,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''
    ],
    'B3': [
        '''CREATE TABLE IF NOT EXISTS prompt_templates (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            template TEXT NOT NULL,
            variables TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''
    ],
    'B4': [
        '''CREATE TABLE IF NOT EXISTS response_cache (
            id INTEGER PRIMARY KEY,
            prompt_hash TEXT UNIQUE NOT NULL,
            response TEXT,
            expires_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''
    ],
    'B5': [
        '''CREATE TABLE IF NOT EXISTS contexts (
            id INTEGER PRIMARY KEY,
            context_type TEXT NOT NULL,
            content TEXT,
            max_tokens INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''
    ],
    'C1': [
        '''CREATE TABLE IF NOT EXISTS commands (
            id INTEGER PRIMARY KEY,
            session_id TEXT NOT NULL,
            command TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''
    ],
    'C2': [
        '''CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP,
            status TEXT
        );'''
    ],
    'C3': [
        '''CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY,
            trigger TEXT NOT NULL,
            suggestion TEXT NOT NULL,
            context TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''
    ],
    'C4': [
        '''CREATE TABLE IF NOT EXISTS error_logs (
            id INTEGER PRIMARY KEY,
            error_type TEXT NOT NULL,
            message TEXT,
            stack_trace TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''
    ],
    'C5': [
        '''CREATE TABLE IF NOT EXISTS preferences (
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            setting_key TEXT NOT NULL,
            setting_value TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''
    ],
    'D1': [
        '''CREATE TABLE IF NOT EXISTS file_operations (
            id INTEGER PRIMARY KEY,
            operation_type TEXT NOT NULL,
            file_path TEXT NOT NULL,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''
    ],
    'D2': [
        '''CREATE TABLE IF NOT EXISTS directory_cache (
            id INTEGER PRIMARY KEY,
            path TEXT NOT NULL,
            parent_path TEXT,
            is_directory BOOLEAN,
            last_modified TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''
    ],
    'D3': [
        '''CREATE TABLE IF NOT EXISTS file_metadata (
            id INTEGER PRIMARY KEY,
            file_path TEXT NOT NULL,
            size INTEGER,
            mime_type TEXT,
            hash TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''
    ],
    'D4': [
        '''CREATE TABLE IF NOT EXISTS permissions (
            id INTEGER PRIMARY KEY,
            file_path TEXT NOT NULL,
            user_id TEXT,
            access_level TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''
    ],
    'D5': [
        '''CREATE TABLE IF NOT EXISTS operation_queue (
            id INTEGER PRIMARY KEY,
            operation_type TEXT NOT NULL,
            parameters TEXT,
            priority INTEGER,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''
    ],
    'E1': [
        '''CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY,
            metric_type TEXT NOT NULL,
            value REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''
    ],
    'E2': [
        '''CREATE TABLE IF NOT EXISTS user_settings (
            id INTEGER PRIMARY KEY,
            user_id TEXT NOT NULL,
            setting_key TEXT NOT NULL,
            setting_value TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''
    ],
    'E3': [
        '''CREATE TABLE IF NOT EXISTS system_configs (
            id INTEGER PRIMARY KEY,
            config_key TEXT NOT NULL,
            config_value TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''
    ],
    'E4': [
        '''CREATE TABLE IF NOT EXISTS backups (
            id INTEGER PRIMARY KEY,
            backup_path TEXT NOT NULL,
            size INTEGER,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''
    ],
    'E5': [
        '''CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY,
            event_type TEXT NOT NULL,
            user_id TEXT,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''
    ],
    'F1': [
        '''CREATE TABLE IF NOT EXISTS usage_metrics (
            id INTEGER PRIMARY KEY,
            feature_name TEXT NOT NULL,
            usage_count INTEGER DEFAULT 0,
            last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );''',
        '''CREATE TABLE IF NOT EXISTS performance_data (
            id INTEGER PRIMARY KEY,
            operation_type TEXT NOT NULL,
            duration_ms INTEGER,
            resource_usage TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''
    ],
    'F2': [
        '''CREATE TABLE IF NOT EXISTS api_metrics (
            id INTEGER PRIMARY KEY,
            endpoint TEXT NOT NULL,
            response_time_ms INTEGER,
            status_code INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''
    ],
    'F3': [
        '''CREATE TABLE IF NOT EXISTS user_analytics (
            id INTEGER PRIMARY KEY,
            user_id TEXT NOT NULL,
            session_duration INTEGER,
            feature_usage TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''
    ],
    'F4': [
        '''CREATE TABLE IF NOT EXISTS error_analytics (
            id INTEGER PRIMARY KEY,
            error_type TEXT NOT NULL,
            frequency INTEGER DEFAULT 1,
            last_occurrence TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            stack_trace TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''
    ],
    'F5': [
        '''CREATE TABLE IF NOT EXISTS resource_usage (
            id INTEGER PRIMARY KEY,
            resource_type TEXT NOT NULL,
            usage_amount REAL,
            usage_limit REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''
    ],
    'G1': [
        '''CREATE TABLE IF NOT EXISTS extensions (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            version TEXT NOT NULL,
            enabled BOOLEAN DEFAULT true,
            config TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''
    ],
    'G2': [
        '''CREATE TABLE IF NOT EXISTS extension_hooks (
            id INTEGER PRIMARY KEY,
            extension_id INTEGER,
            hook_type TEXT NOT NULL,
            priority INTEGER DEFAULT 0,
            handler TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (extension_id) REFERENCES extensions(id)
        );'''
    ],
    'G3': [
        '''CREATE TABLE IF NOT EXISTS extension_dependencies (
            id INTEGER PRIMARY KEY,
            extension_id INTEGER,
            dependency_name TEXT NOT NULL,
            required_version TEXT,
            optional BOOLEAN DEFAULT false,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (extension_id) REFERENCES extensions(id)
        );'''
    ],
    'G4': [
        '''CREATE TABLE IF NOT EXISTS extension_logs (
            id INTEGER PRIMARY KEY,
            extension_id INTEGER,
            log_level TEXT NOT NULL,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (extension_id) REFERENCES extensions(id)
        );'''
    ],
    'G5': [
        '''CREATE TABLE IF NOT EXISTS extension_data (
            id INTEGER PRIMARY KEY,
            extension_id INTEGER,
            data_key TEXT NOT NULL,
            data_value TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (extension_id) REFERENCES extensions(id)
        );'''
    ]
}