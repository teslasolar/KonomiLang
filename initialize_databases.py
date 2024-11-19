"""
Database Grid Initialization with Schema Version Control
"""
import os
import sqlite3
from pathlib import Path
from konomi.utils.schema_manager import SchemaManager
from typing import List, Dict
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('schema_operations.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def initialize_database(db_path: Path, schema_queries: List[str]) -> bool:
    """Initialize a single database with its schema."""
    try:
        # Ensure directory exists
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create schema version control tables first
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schema_versions (
                id INTEGER PRIMARY KEY,
                version INTEGER NOT NULL,
                description TEXT,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                script_name TEXT,
                checksum TEXT,
                status TEXT DEFAULT 'success'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schema_migrations (
                id INTEGER PRIMARY KEY,
                version INTEGER NOT NULL,
                script TEXT NOT NULL,
                dependencies TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info(f"Successfully initialized {db_path}")
        return True
    except Exception as e:
        logger.error(f"Error initializing {db_path}: {str(e)}")
        return False

def create_migration_script(schema_queries: List[str]) -> str:
    """Create a properly formatted migration script from schema queries."""
    try:
        script_parts = ["PRAGMA foreign_keys = ON;"]
        
        # Add each schema query, properly formatted
        for query in schema_queries:
            # Remove any trailing semicolons and extra whitespace
            clean_query = query.strip().rstrip(';')
            script_parts.append(clean_query + ";")
        
        # Join all parts with proper spacing
        return "\n\n".join(script_parts)
    except Exception as e:
        logger.error(f"Error creating migration script: {str(e)}")
        raise

def main():
    base_dir = Path("db_grid")
    success_count = 0
    total_dbs = 35
    failed_dbs = []
    
    # Initialize schema manager
    schema_manager = SchemaManager(base_dir)
    
    try:
        # Initialize each database
        for row in 'ABCDEFG':
            for col in range(1, 6):
                position = f"{row}{col}"
                db_path = base_dir / position / "database.db"
                
                if position in SCHEMAS:
                    try:
                        logger.info(f"Initializing database {position}...")
                        
                        # Step 1: Initialize database with empty schema
                        if initialize_database(db_path, []):
                            try:
                                # Step 2: Clean existing migrations if any
                                schema_manager.clean_migrations(db_path)
                                
                                # Step 3: Create migration script
                                migration_script = create_migration_script(SCHEMAS[position])
                                
                                logger.info(f"Registering migration for database {position}")
                                if schema_manager.register_migration(db_path, 1, migration_script, [], force=True):
                                    try:
                                        # Step 4: Apply migration
                                        logger.info(f"Applying migration for database {position}")
                                        if schema_manager.apply_migration(db_path, 1, f"Initial schema for {position}", force=True):
                                            success_count += 1
                                            logger.info(f"Successfully applied migration for database {position}")
                                        else:
                                            failed_dbs.append((position, "Failed to apply migration"))
                                            logger.error(f"Failed to apply migration for database {position}")
                                    except Exception as e:
                                        failed_dbs.append((position, f"Migration error: {str(e)}"))
                                        logger.error(f"Error applying migration for {position}: {str(e)}")
                                else:
                                    failed_dbs.append((position, "Failed to register migration"))
                                    logger.error(f"Failed to register migration for database {position}")
                            except Exception as e:
                                failed_dbs.append((position, f"Registration error: {str(e)}"))
                                logger.error(f"Error registering migration for {position}: {str(e)}")
                        else:
                            failed_dbs.append((position, "Failed to initialize database"))
                            logger.error(f"Failed to initialize database {position}")
                    except Exception as e:
                        failed_dbs.append((position, f"Error: {str(e)}"))
                        logger.error(f"Critical error for database {position}: {str(e)}")
                else:
                    logger.warning(f"No schema defined for database {position}")
        
        # Print initialization summary
        print("\nInitialization Summary:")
        print(f"Successfully initialized {success_count} out of {total_dbs} databases")
        
        if failed_dbs:
            print("\nFailed Databases:")
            for db, reason in failed_dbs:
                print(f"Database {db}: {reason}")
        
        return success_count == total_dbs
        
    except Exception as e:
        logger.error(f"Critical error during initialization: {str(e)}")
        return False

if __name__ == "__main__":
    # Import schemas here to avoid circular import
    from database.schemas import SCHEMAS
    main()
