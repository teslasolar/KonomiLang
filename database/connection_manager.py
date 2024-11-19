"""
Database connection manager for the Konomi database grid.
Provides centralized connection handling and pooling for all databases.
"""
import os
import sqlite3
import threading
import time
from typing import Dict, Optional, List
from contextlib import contextmanager

class DatabaseConnectionManager:
    def __init__(self, base_dir: str = "db_grid", max_pool_size: int = 5, retry_attempts: int = 3):
        self.base_dir = base_dir
        self.max_pool_size = max_pool_size
        self.retry_attempts = retry_attempts
        self._connection_pools: Dict[str, List[sqlite3.Connection]] = {}
        self._lock = threading.Lock()
        self._error_counts: Dict[str, int] = {}
        
    def _get_db_path(self, position: str) -> str:
        """Get the full path for a database position."""
        return os.path.join(self.base_dir, position, "database.db")
        
    @contextmanager
    def get_connection(self, position: str) -> sqlite3.Connection:
        """Get a database connection from the pool with automatic return."""
        conn = self._acquire_connection(position)
        try:
            yield conn
        finally:
            self._return_connection(position, conn)
            
    def _acquire_connection(self, position: str) -> sqlite3.Connection:
        """Get a connection from the pool or create a new one."""
        db_path = self._get_db_path(position)
        
        for attempt in range(self.retry_attempts):
            try:
                with self._lock:
                    # Initialize pool if needed
                    if position not in self._connection_pools:
                        self._connection_pools[position] = []
                    
                    # Try to get existing connection
                    while self._connection_pools[position]:
                        conn = self._connection_pools[position].pop()
                        try:
                            # Test if connection is still valid
                            conn.execute("SELECT 1")
                            return conn
                        except sqlite3.Error:
                            conn.close()
                    
                    # Create new connection
                    conn = sqlite3.connect(db_path)
                    conn.row_factory = sqlite3.Row  # Enable row factory for named columns
                    return conn
                    
            except sqlite3.Error as e:
                if attempt == self.retry_attempts - 1:
                    raise ConnectionError(f"Failed to connect to database {position} after {self.retry_attempts} attempts: {str(e)}")
                time.sleep(0.1 * (attempt + 1))  # Exponential backoff
                
    def _return_connection(self, position: str, conn: sqlite3.Connection):
        """Return a connection to the pool."""
        try:
            with self._lock:
                if len(self._connection_pools.get(position, [])) < self.max_pool_size:
                    self._connection_pools[position].append(conn)
                else:
                    conn.close()
        except Exception:
            conn.close()
            
    def execute_query(self, position: str, query: str, parameters: tuple = ()) -> List[sqlite3.Row]:
        """Execute a query and return results."""
        with self.get_connection(position) as conn:
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            return cursor.fetchall()
            
    def execute_write(self, position: str, query: str, parameters: tuple = ()):
        """Execute a write query (INSERT, UPDATE, DELETE)."""
        with self.get_connection(position) as conn:
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            conn.commit()
            
    def execute_many(self, position: str, query: str, parameters: List[tuple]):
        """Execute many write operations in a single transaction."""
        with self.get_connection(position) as conn:
            cursor = conn.cursor()
            cursor.executemany(query, parameters)
            conn.commit()
            
    def get_table_names(self, position: str) -> List[str]:
        """Get list of tables in the database."""
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        return [row['name'] for row in self.execute_query(position, query)]
        
    def check_connection(self, position: str) -> bool:
        """Test if connection to database is possible."""
        try:
            with self.get_connection(position):
                return True
        except Exception:
            return False
            
    def close_all_connections(self):
        """Close all connections in all pools."""
        with self._lock:
            for pool in self._connection_pools.values():
                for conn in pool:
                    try:
                        conn.close()
                    except Exception:
                        pass
            self._connection_pools.clear()
