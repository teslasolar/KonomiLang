"""
Database Grid Initialization with Schema Version Control
"""
import os
import sqlite3
from pathlib import Path
from konomi.utils.schema_manager import SchemaManager
from typing import List, Dict, Tuple, Optional
import logging
from dataclasses import dataclass

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

@dataclass
class DatabaseConfig:
    """Configuration for database initialization."""
    position: str
    path: Path
    schema: Optional[List[str]] = None

class SchemaInitializer:
    """Handles schema initialization and migration."""
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.schema_manager = SchemaManager(base_dir)

    def create_version_control_tables(self, cursor: sqlite3.Cursor) -> None:
        """Create schema version control tables."""
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

    def initialize_database(self, db_config: DatabaseConfig) -> bool:
        """Initialize a single database with its schema."""
        try:
            db_config.path.parent.mkdir(parents=True, exist_ok=True)
            
            conn = sqlite3.connect(db_config.path)
            cursor = conn.cursor()
            
            self.create_version_control_tables(cursor)
            
            conn.commit()
            conn.close()
            logger.info(f"Successfully initialized {db_config.path}")
            return True
        except Exception as e:
            logger.error(f"Error initializing {db_config.path}: {str(e)}")
            return False

    def create_migration_script(self, schema_queries: List[str]) -> str:
        """Create a properly formatted migration script from schema queries."""
        try:
            script_parts = ["PRAGMA foreign_keys = ON;"]
            script_parts.extend(query.strip().rstrip(';') + ";" for query in schema_queries)
            return "\n\n".join(script_parts)
        except Exception as e:
            logger.error(f"Error creating migration script: {str(e)}")
            raise

    def apply_schema_migration(self, db_config: DatabaseConfig) -> Tuple[bool, Optional[str]]:
        """Apply schema migration to a database."""
        try:
            if not db_config.schema:
                return True, None

            # Clean existing migrations
            self.schema_manager.clean_migrations(db_config.path)
            
            # Create and register migration
            migration_script = self.create_migration_script(db_config.schema)
            if not self.schema_manager.register_migration(db_config.path, 1, migration_script, [], force=True):
                return False, "Failed to register migration"
            
            # Apply migration
            if not self.schema_manager.apply_migration(db_config.path, 1, f"Initial schema for {db_config.position}", force=True):
                return False, "Failed to apply migration"
            
            return True, None
        except Exception as e:
            return False, str(e)

class GridInitializer:
    """Manages the initialization of the entire database grid."""
    def __init__(self, base_dir: Path, schemas: Dict[str, List[str]]):
        self.base_dir = base_dir
        self.schemas = schemas
        self.schema_initializer = SchemaInitializer(base_dir)
        self.failed_dbs: List[Tuple[str, str]] = []
        self.success_count = 0

    def create_db_config(self, position: str) -> DatabaseConfig:
        """Create database configuration for a position."""
        return DatabaseConfig(
            position=position,
            path=self.base_dir / position / "database.db",
            schema=self.schemas.get(position)
        )

    def initialize_single_database(self, config: DatabaseConfig) -> bool:
        """Initialize a single database with error handling."""
        try:
            if not self.schema_initializer.initialize_database(config):
                self.failed_dbs.append((config.position, "Failed to initialize database"))
                return False

            if config.schema:
                success, error = self.schema_initializer.apply_schema_migration(config)
                if not success:
                    self.failed_dbs.append((config.position, error or "Unknown error"))
                    return False

            self.success_count += 1
            return True
        except Exception as e:
            self.failed_dbs.append((config.position, f"Error: {str(e)}"))
            logger.error(f"Critical error for database {config.position}: {str(e)}")
            return False

    def initialize_grid(self) -> bool:
        """Initialize all databases in the grid."""
        total_dbs = 35
        
        try:
            for row in 'ABCDEFG':
                for col in range(1, 6):
                    position = f"{row}{col}"
                    config = self.create_db_config(position)
                    
                    if position in self.schemas:
                        logger.info(f"Initializing database {position}...")
                        self.initialize_single_database(config)
                    else:
                        logger.warning(f"No schema defined for database {position}")
            
            self.print_summary(total_dbs)
            return self.success_count == total_dbs
            
        except Exception as e:
            logger.error(f"Critical error during initialization: {str(e)}")
            return False

    def print_summary(self, total_dbs: int) -> None:
        """Print initialization summary."""
        print("\nInitialization Summary:")
        print(f"Successfully initialized {self.success_count} out of {total_dbs} databases")
        
        if self.failed_dbs:
            print("\nFailed Databases:")
            for db, reason in self.failed_dbs:
                print(f"Database {db}: {reason}")

def main():
    # Import schemas here to avoid circular import
    from database.schemas import SCHEMAS
    
    base_dir = Path("db_grid")
    initializer = GridInitializer(base_dir, SCHEMAS)
    return initializer.initialize_grid()

if __name__ == "__main__":
    main()
