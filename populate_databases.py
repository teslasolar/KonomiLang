import os
import sqlite3
import json
from datetime import datetime, timedelta

def connect_to_db(position):
    """Connect to a specific database in the grid."""
    db_path = f"db_grid/{position}/database.db"
    return sqlite3.connect(db_path)

def populate_lexer_tokens(conn):
    """Populate A1 database with basic token patterns."""
    cursor = conn.cursor()
    tokens = [
        ('KEYWORD', r'\b(if|else|while|for|def|return|true|false)\b', 10, 'Language keywords'),
        ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*', 5, 'Variable or function names'),
        ('NUMBER', r'\d+(\.\d+)?', 5, 'Numeric literals'),
        ('STRING', r'"[^"]*"', 5, 'String literals'),
        ('OPERATOR', r'[+\-*/=<>!]=?', 8, 'Operators'),
        ('PARENTHESIS', r'[()]', 9, 'Parentheses'),
        ('WHITESPACE', r'\s+', 1, 'Whitespace characters')
    ]
    cursor.executemany(
        'INSERT INTO tokens (token_type, pattern, priority, description) VALUES (?, ?, ?, ?)',
        tokens
    )
    conn.commit()

def populate_parser_rules(conn):
    """Populate A2 database with basic parsing rules."""
    cursor = conn.cursor()
    rules = [
        ('program', 'statement_list', 1),
        ('statement_list', 'statement | statement_list statement', 2),
        ('statement', 'expression | assignment | if_statement | while_statement', 3),
        ('expression', 'term | expression operator term', 4),
        ('assignment', 'IDENTIFIER EQUALS expression', 5)
    ]
    cursor.executemany(
        'INSERT INTO parser_rules (rule_name, production, precedence) VALUES (?, ?, ?)',
        rules
    )
    conn.commit()

def populate_model_configs(conn):
    """Populate B2 database with default model configurations."""
    cursor = conn.cursor()
    configs = [
        ('gpt-4', json.dumps({
            'max_tokens': 2048,
            'temperature': 0.7,
            'top_p': 1,
            'frequency_penalty': 0,
            'presence_penalty': 0
        }), True),
        ('gpt-3.5-turbo', json.dumps({
            'max_tokens': 1024,
            'temperature': 0.8,
            'top_p': 1,
            'frequency_penalty': 0,
            'presence_penalty': 0
        }), True)
    ]
    cursor.executemany(
        'INSERT INTO model_configs (model_name, parameters, active) VALUES (?, ?, ?)',
        configs
    )
    conn.commit()

def populate_prompt_templates(conn):
    """Populate B3 database with standard prompt templates."""
    cursor = conn.cursor()
    templates = [
        ('code_completion', 'Complete the following code:\n{code}\n', '["code"]'),
        ('error_explanation', 'Explain the following error:\n{error}\n', '["error"]'),
        ('code_review', 'Review the following code changes:\n{changes}\n', '["changes"]'),
        ('documentation', 'Generate documentation for:\n{code}\n', '["code"]')
    ]
    cursor.executemany(
        'INSERT INTO prompt_templates (name, template, variables) VALUES (?, ?, ?)',
        templates
    )
    conn.commit()

def populate_system_configs(conn):
    """Populate E3 database with default system configurations."""
    cursor = conn.cursor()
    configs = [
        ('max_tokens_per_request', '4096'),
        ('default_model', 'gpt-3.5-turbo'),
        ('cache_duration', '3600'),
        ('max_history_size', '1000'),
        ('debug_mode', 'false')
    ]
    cursor.executemany(
        'INSERT INTO system_configs (config_key, config_value) VALUES (?, ?)',
        configs
    )
    conn.commit()

def main():
    # Dictionary mapping positions to their initialization functions
    initializers = {
        'A1': populate_lexer_tokens,
        'A2': populate_parser_rules,
        'B2': populate_model_configs,
        'B3': populate_prompt_templates,
        'E3': populate_system_configs
    }
    
    success_count = 0
    total_initializations = len(initializers)
    
    for position, init_func in initializers.items():
        try:
            conn = connect_to_db(position)
            init_func(conn)
            conn.close()
            print(f"Successfully populated database {position}")
            success_count += 1
        except Exception as e:
            print(f"Error populating database {position}: {str(e)}")
    
    print(f"\nPopulation complete:")
    print(f"Successfully populated {success_count}/{total_initializations} databases")
    return success_count == total_initializations

if __name__ == "__main__":
    if main():
        print("Success: All databases populated successfully!")
        exit(0)
    else:
        print("Error: Some databases were not populated properly.")
        exit(1)
