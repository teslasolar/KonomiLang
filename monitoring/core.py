"""
Core monitoring functionality for the database grid.
"""
import os
import sqlite3
import time
from datetime import datetime
import json
from typing import Dict, Any, Optional
import threading

class DatabaseMonitor:
    def __init__(self, base_dir="db_grid"):
        self.base_dir = base_dir
        self.metrics_db = os.path.join(base_dir, "E1", "database.db")
        self.lock = threading.Lock()
        self._connection_pools: Dict[str, list] = {}
        self._error_counts: Dict[str, int] = {}
        
    def _get_connection(self, db_path: str) -> sqlite3.Connection:
        """Get a connection from the pool or create a new one."""
        with self.lock:
            if db_path not in self._connection_pools:
                self._connection_pools[db_path] = []
            
            # Try to get an existing connection
            while self._connection_pools[db_path]:
                conn = self._connection_pools[db_path].pop()
                try:
                    # Test if connection is still valid
                    conn.execute("SELECT 1")
                    return conn
                except sqlite3.Error:
                    conn.close()
            
            # Create new connection if none available
            return sqlite3.connect(db_path)
            
    def _return_connection(self, db_path: str, conn: sqlite3.Connection):
        """Return a connection to the pool."""
        with self.lock:
            if len(self._connection_pools.get(db_path, [])) < 5:  # Max pool size
                self._connection_pools[db_path].append(conn)
            else:
                conn.close()

    def check_connection(self, db_path: str) -> bool:
        """Test database connection and return status."""
        try:
            conn = self._get_connection(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            self._return_connection(db_path, conn)
            return True
        except sqlite3.Error:
            self._increment_error_count(db_path)
            return False
            
    def get_db_size(self, db_path: str) -> int:
        """Get database file size in bytes."""
        try:
            return os.path.getsize(db_path)
        except OSError:
            self._increment_error_count(db_path)
            return 0
            
    def check_table_integrity(self, db_path: str) -> bool:
        """Check database table integrity."""
        try:
            conn = self._get_connection(db_path)
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()[0]
            self._return_connection(db_path, conn)
            return result == "ok"
        except sqlite3.Error:
            self._increment_error_count(db_path)
            return False
            
    def get_table_counts(self, db_path: str) -> Dict[str, int]:
        """Get record counts for all tables in database."""
        counts = {}
        try:
            conn = self._get_connection(db_path)
            cursor = conn.cursor()
            
            # Get list of tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            # Count records in each table
            for (table_name,) in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                counts[table_name] = count
                
            self._return_connection(db_path, conn)
            return counts
        except sqlite3.Error:
            self._increment_error_count(db_path)
            return {}

    def track_query_performance(self, db_path: str, query: str) -> Dict[str, Any]:
        """Track query execution time and performance."""
        try:
            conn = self._get_connection(db_path)
            cursor = conn.cursor()
            
            start_time = time.time()
            cursor.execute(f"EXPLAIN QUERY PLAN {query}")
            query_plan = cursor.fetchall()
            
            cursor.execute(query)
            results = cursor.fetchall()
            end_time = time.time()
            
            execution_time = end_time - start_time
            
            self._return_connection(db_path, conn)
            
            return {
                "execution_time": execution_time,
                "query_plan": query_plan,
                "result_count": len(results)
            }
        except sqlite3.Error as e:
            self._increment_error_count(db_path)
            return {
                "error": str(e),
                "execution_time": None,
                "query_plan": None,
                "result_count": None
            }

    def get_lock_info(self, db_path: str) -> Dict[str, Any]:
        """Get information about database locks."""
        try:
            conn = self._get_connection(db_path)
            cursor = conn.cursor()
            
            cursor.execute("PRAGMA database_list")
            databases = cursor.fetchall()
            
            lock_info = {}
            for db in databases:
                cursor.execute(f"PRAGMA {db[1]}.lock_status")
                lock_info[db[1]] = cursor.fetchall()
            
            self._return_connection(db_path, conn)
            return lock_info
        except sqlite3.Error:
            self._increment_error_count(db_path)
            return {}

    def _increment_error_count(self, db_path: str):
        """Increment error count for a database."""
        with self.lock:
            self._error_counts[db_path] = self._error_counts.get(db_path, 0) + 1

    def get_error_rate(self, db_path: str) -> Dict[str, Any]:
        """Get error statistics for a database."""
        with self.lock:
            return {
                "total_errors": self._error_counts.get(db_path, 0),
                "has_recent_errors": self._error_counts.get(db_path, 0) > 0
            }

    def get_connection_pool_status(self, db_path: str) -> Dict[str, Any]:
        """Get status of the connection pool."""
        with self.lock:
            pool = self._connection_pools.get(db_path, [])
            return {
                "pool_size": len(pool),
                "max_pool_size": 5,
                "available_connections": len(pool)
            }
            
    def store_metrics(self, position: str, metrics: Dict[str, Any]):
        """Store monitoring metrics in E1 database."""
        try:
            conn = self._get_connection(self.metrics_db)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO metrics (metric_type, value)
                VALUES (?, ?)
            """, (
                f"db_status_{position}",
                json.dumps(metrics)
            ))
            
            conn.commit()
            self._return_connection(self.metrics_db, conn)
        except sqlite3.Error as e:
            print(f"Error storing metrics: {str(e)}")
            
    def monitor_databases(self) -> Dict[str, Dict[str, Any]]:
        """Monitor all databases in the grid."""
        results = {}
        
        for row in 'ABCDEFG':
            for col in range(1, 6):
                position = f"{row}{col}"
                db_path = os.path.join(self.base_dir, position, "database.db")
                
                # Basic metrics
                metrics = {
                    "timestamp": datetime.now().isoformat(),
                    "connection_status": self.check_connection(db_path),
                    "size_bytes": self.get_db_size(db_path),
                    "integrity_check": self.check_table_integrity(db_path),
                    "table_counts": self.get_table_counts(db_path)
                }
                
    def get_function_performance_metrics(self) -> Dict[str, Any]:
        """Get function performance metrics."""
        try:
            from konomi.utils.performance import _metrics
            slow_functions = _metrics.get_slow_functions(threshold=1.0)
            recent_errors = self.connection_manager.execute_query(
                "E1",
                """
                SELECT function_name, error_type, COUNT(*) as error_count
                FROM function_metrics
                WHERE success = 0 AND timestamp > datetime('now', '-1 day')
                GROUP BY function_name, error_type
                """)
            
            return {
                "slow_functions": slow_functions,
                "recent_errors": recent_errors
            }
        except Exception as e:
            logger.error(f"Error getting function metrics: {str(e)}")
            return {}
                # Advanced metrics
            metrics.update({
                "error_stats": self.get_error_rate(db_path),
                "connection_pool": self.get_connection_pool_status(db_path),
                "lock_info": self.get_lock_info(db_path)
            })
            
            # Track performance of a simple query
            metrics["query_performance"] = self.track_query_performance(
                db_path,
                "SELECT COUNT(*) FROM sqlite_master"
            )
            
            # Add function performance metrics
            if position == "E1":  # Store function metrics only in E1 summary
                metrics["function_performance"] = self.get_function_performance_metrics()
            
            results[position] = metrics
            self.store_metrics(position, metrics)
                
        return results
