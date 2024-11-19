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

    def clean_migrations(self, db_path: Path) -> bool:
        """Remove all existing migrations from a database"""
        conn = None
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Remove all existing migrations
            cursor.execute("DELETE FROM schema_migrations")
            cursor.execute("DELETE FROM schema_versions")
            
            conn.commit()
            logger.info(f"Cleaned migrations from {db_path}")
            return True
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Failed to clean migrations: {str(e)}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as e:
                    logger.error(f"Error closing connection: {str(e)}")

    def _init_version_control(self, db_path: Path) -> bool:
        """Initialize schema version control table in a database"""
        conn = None
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Create version control tables
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
            logger.info(f"Initialized version control in {db_path}")
            return True
                
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Failed to initialize version control in {db_path}: {str(e)}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as e:
                    logger.error(f"Error closing connection: {str(e)}")

    def _validate_sql_script(self, script: str) -> bool:
        """Validate SQL script format and syntax"""
        conn = None
        try:
            conn = sqlite3.connect(':memory:')
            cursor = conn.cursor()
            
            # Split statements and validate each one
            statements = [stmt.strip() for stmt in script.split(';') if stmt.strip()]
            
            # Start a transaction for validation
            cursor.execute("BEGIN")
            
            for statement in statements:
                try:
                    cursor.execute(statement)
                except sqlite3.Error as e:
                    cursor.execute("ROLLBACK")
                    logger.error(f"SQL validation failed for statement '{statement}': {str(e)}")
                    return False
            
            cursor.execute("COMMIT")
            return True
            
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
                         dependencies: Optional[List[int]] = None, force: bool = False) -> bool:
        """Register a new migration script"""
        # First validate the SQL script
        if not self._validate_sql_script(script):
            logger.error("Failed to validate migration script")
            return False
            
        conn = None
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check if version exists and force flag is set
            cursor.execute("SELECT version FROM schema_migrations WHERE version = ?", (version,))
            if cursor.fetchone():
                if force:
                    # Remove existing migration if force is True
                    cursor.execute("DELETE FROM schema_migrations WHERE version = ?", (version,))
                    cursor.execute("DELETE FROM schema_versions WHERE version = ?", (version,))
                else:
                    raise ValueError(f"Migration version {version} already exists")
            
            # Start transaction for registration
            cursor.execute("BEGIN")
            
            # Insert migration with parameterized query
            cursor.execute(
                "INSERT INTO schema_migrations (version, script, dependencies) VALUES (?, ?, ?)",
                (version, script, json.dumps(dependencies or []))
            )
            
            cursor.execute("COMMIT")
            logger.info(f"Registered migration version {version} for {db_path}")
            return True
                
        except Exception as e:
            if conn:
                cursor.execute("ROLLBACK")
            logger.error(f"Failed to register migration: {str(e)}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as e:
                    logger.error(f"Error closing connection: {str(e)}")

    def apply_migration(self, db_path: Path, version: int, description: str = "", force: bool = False) -> bool:
        """Apply a specific migration version to a database"""
        conn = None
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get migration script and dependencies
            cursor.execute(
                "SELECT script, dependencies FROM schema_migrations WHERE version = ?",
                (version,)
            )
            result = cursor.fetchone()
            
            if not result:
                raise ValueError(f"Migration version {version} not found")
                
            script, dependencies = result
            deps = json.loads(dependencies)
            
            # Check if already applied unless force flag is set
            cursor.execute("SELECT version FROM schema_versions WHERE version = ?", (version,))
            if cursor.fetchone() and not force:
                raise ValueError(f"Migration version {version} already applied")
            
            # Check dependencies unless force flag is set
            if not force:
                for dep_version in deps:
                    cursor.execute(
                        "SELECT id FROM schema_versions WHERE version = ? AND status = 'success'",
                        (dep_version,)
                    )
                    if not cursor.fetchone():
                        raise ValueError(f"Dependency version {dep_version} not applied")
            
            # Start transaction for migration
            cursor.execute("BEGIN")
            
            try:
                # Split and execute each statement
                statements = [stmt.strip() for stmt in script.split(';') if stmt.strip()]
                for statement in statements:
                    cursor.execute(statement)
                
                # Record version
                if force:
                    cursor.execute("DELETE FROM schema_versions WHERE version = ?", (version,))
                    
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
                raise Exception(f"Failed to execute migration: {str(e)}")
                
        except Exception as e:
            logger.error(f"Failed to apply migration: {str(e)}")
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
                try:
                    conn.close()
                except Exception as e:
                    logger.error(f"Error closing connection: {str(e)}")

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
                try:
                    conn.close()
                except Exception as e:
                    logger.error(f"Error closing connection: {str(e)}")

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
                try:
                    conn.close()
                except Exception as e:
                    logger.error(f"Error closing connection: {str(e)}")
