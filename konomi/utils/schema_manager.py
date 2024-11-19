"""
Schema Version Control Manager for KonomiLang Database Grid
Handles database schema versioning and migrations
"""
import sqlite3
from pathlib import Path
import json
import logging
from typing import Dict, List, Optional, Union
from datetime import datetime

logger = logging.getLogger(__name__)

class SchemaManager:
    def __init__(self, base_dir: Union[str, Path] = "db_grid"):
        self.base_dir = Path(base_dir)
        self._setup_logging()
        
    def _setup_logging(self):
        """Configure logging for schema operations"""
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler = logging.FileHandler('schema_operations.log')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    
    def _init_version_control(self, db_path: Path) -> bool:
        """Initialize schema version control table in a database"""
        conn = None
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Enable foreign keys and begin transaction
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute("BEGIN TRANSACTION")
            
            try:
                # Create version control tables
                cursor.executescript('''
                    CREATE TABLE IF NOT EXISTS schema_versions (
                        id INTEGER PRIMARY KEY,
                        version INTEGER NOT NULL,
                        description TEXT,
                        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        script_name TEXT,
                        checksum TEXT,
                        status TEXT DEFAULT 'success'
                    );
                    
                    CREATE TABLE IF NOT EXISTS schema_migrations (
                        id INTEGER PRIMARY KEY,
                        version INTEGER NOT NULL,
                        script TEXT NOT NULL,
                        dependencies TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                ''')
                
                cursor.execute("COMMIT")
                logger.info(f"Initialized version control in {db_path}")
                return True
                
            except Exception as e:
                cursor.execute("ROLLBACK")
                logger.error(f"Failed to create version control tables: {str(e)}")
                raise
                
        except Exception as e:
            logger.error(f"Failed to initialize version control in {db_path}: {str(e)}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as e:
                    logger.error(f"Error closing connection: {str(e)}")
    
    def get_current_version(self, db_path: Path) -> int:
        """Get the current schema version of a database"""
        conn = None
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT MAX(version) FROM schema_versions WHERE status = 'success'")
            version = cursor.fetchone()[0]
            
            return version or 0
        except Exception as e:
            logger.error(f"Failed to get current version for {db_path}: {str(e)}")
            return 0
        finally:
            if conn:
                conn.close()

    def _validate_sql_script(self, script: str) -> bool:
        """Validate SQL script format and syntax"""
        conn = None
        try:
            conn = sqlite3.connect(':memory:')
            cursor = conn.cursor()
            
            # Enable foreign keys and begin transaction
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute("BEGIN TRANSACTION")
            
            try:
                # Execute script within transaction
                for statement in script.split(';'):
                    if statement.strip():
                        cursor.execute(statement)
                
                cursor.execute("COMMIT")
                return True
                
            except sqlite3.Error as e:
                cursor.execute("ROLLBACK")
                logger.error(f"SQL validation failed: {str(e)}")
                return False
                
        except Exception as e:
            logger.error(f"Unexpected error during SQL validation: {str(e)}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as e:
                    logger.error(f"Error closing validation connection: {str(e)}")
    
    def register_migration(self, db_path: Path, version: int, script: str, 
                         dependencies: Optional[List[int]] = None) -> bool:
        """Register a new migration script"""
        conn = None
        try:
            # Validate SQL script before registering
            if not self._validate_sql_script(script):
                raise ValueError("Invalid SQL script")

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Enable foreign keys and begin transaction
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute("BEGIN TRANSACTION")
            
            try:
                # Insert migration with parameterized query
                cursor.execute(
                    "INSERT INTO schema_migrations (version, script, dependencies) VALUES (?, ?, ?)",
                    (version, script, json.dumps(dependencies or []))
                )
                
                cursor.execute("COMMIT")
                logger.info(f"Registered migration version {version} for {db_path}")
                return True
                
            except Exception as e:
                cursor.execute("ROLLBACK")
                logger.error(f"Failed to register migration: {str(e)}")
                raise
                
        except Exception as e:
            logger.error(f"Failed to register migration for {db_path}: {str(e)}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as e:
                    logger.error(f"Error closing connection: {str(e)}")
    
    def apply_migration(self, db_path: Path, version: int, description: str = "") -> bool:
        """Apply a specific migration version to a database"""
        conn = None
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Enable foreign keys
            cursor.execute("PRAGMA foreign_keys = ON")
            
            # Get migration script
            cursor.execute(
                "SELECT script, dependencies FROM schema_migrations WHERE version = ?",
                (version,)
            )
            result = cursor.fetchone()
            
            if not result:
                raise ValueError(f"Migration version {version} not found")
                
            script, dependencies = result
            deps = json.loads(dependencies)
            
            # Check dependencies
            for dep_version in deps:
                cursor.execute(
                    "SELECT id FROM schema_versions WHERE version = ? AND status = 'success'",
                    (dep_version,)
                )
                if not cursor.fetchone():
                    raise ValueError(f"Dependency version {dep_version} not applied")
            
            # Begin transaction before executing migration
            cursor.execute("BEGIN TRANSACTION")
            
            try:
                # Execute each statement in the script
                for statement in script.split(';'):
                    if statement.strip():
                        cursor.execute(statement)
                
                # Record version
                cursor.execute(
                    """INSERT INTO schema_versions 
                       (version, description, script_name, status) 
                       VALUES (?, ?, ?, ?)""",
                    (version, description, f"migration_{version}.sql", 'success')
                )
                
                cursor.execute("COMMIT")
                logger.info(f"Applied migration version {version} to {db_path}")
                return True
                
            except Exception as e:
                cursor.execute("ROLLBACK")
                logger.error(f"Failed to execute migration script: {str(e)}")
                raise
            
        except Exception as e:
            logger.error(f"Failed to apply migration to {db_path}: {str(e)}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as e:
                    logger.error(f"Error closing connection: {str(e)}")
    
    def init_all_databases(self) -> Dict[str, bool]:
        """Initialize version control in all databases in the grid"""
        results = {}
        try:
            for row in 'ABCDEFG':
                for col in range(1, 6):
                    position = f"{row}{col}"
                    db_path = self.base_dir / position / "database.db"
                    results[position] = self._init_version_control(db_path)
            return results
        except Exception as e:
            logger.error(f"Failed to initialize all databases: {str(e)}")
            return results
    
    def get_pending_migrations(self, db_path: Path) -> List[int]:
        """Get list of pending migration versions for a database"""
        conn = None
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT m.version
                FROM schema_migrations m
                LEFT JOIN schema_versions v ON m.version = v.version
                WHERE v.version IS NULL
                ORDER BY m.version
            """)
            
            pending = [row[0] for row in cursor.fetchall()]
            return pending
        except Exception as e:
            logger.error(f"Failed to get pending migrations for {db_path}: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()
    
    def get_migration_history(self, db_path: Path) -> List[Dict]:
        """Get migration history for a database"""
        conn = None
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT version, description, applied_at, status
                FROM schema_versions
                ORDER BY version DESC
            """)
            
            history = []
            for row in cursor.fetchall():
                history.append({
                    'version': row[0],
                    'description': row[1],
                    'applied_at': row[2],
                    'status': row[3]
                })
            
            return history
        except Exception as e:
            logger.error(f"Failed to get migration history for {db_path}: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()
