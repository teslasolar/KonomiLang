"""
Performance metrics collection utilities.
"""
import time
import functools
import threading
import logging
import sqlite3
from typing import Any, Dict, Optional, Callable, List
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Database path for metrics
METRICS_DB_PATH = Path("db_grid/E1/database.db")

class PerformanceMetrics:
    """Handles collection and storage of function performance metrics."""
    
    def __init__(self):
        self.lock = threading.Lock()
        self._initialize_metrics_table()
        
    def _get_connection(self):
        """Get a direct connection to the metrics database."""
        try:
            if not METRICS_DB_PATH.parent.exists():
                METRICS_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
            return sqlite3.connect(str(METRICS_DB_PATH))
        except Exception as e:
            logger.error(f"Failed to connect to metrics database: {str(e)}")
            return None
        
    def _initialize_metrics_table(self):
        """Initialize performance metrics table in E1 database."""
        try:
            conn = self._get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS function_metrics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        function_name TEXT NOT NULL,
                        execution_time REAL NOT NULL,
                        success BOOLEAN NOT NULL,
                        error_type TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        additional_data TEXT
                    )
                """)
                conn.commit()
                conn.close()
        except Exception as e:
            logger.error(f"Failed to initialize metrics table: {str(e)}")
            
    def record_metric(self, function_name: str, execution_time: float, 
                     success: bool = True, error_type: Optional[str] = None,
                     additional_data: Optional[Dict] = None):
        """Record a function's performance metric."""
        try:
            conn = self._get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO function_metrics 
                    (function_name, execution_time, success, error_type, additional_data)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    function_name, execution_time, success, error_type,
                    str(additional_data) if additional_data else None
                ))
                conn.commit()
                conn.close()
        except Exception as e:
            logger.error(f"Failed to record metric for {function_name}: {str(e)}")
            
    def get_function_metrics(self, function_name: str, 
                           limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent metrics for a specific function."""
        query = """
        SELECT * FROM function_metrics 
        WHERE function_name = ? 
        ORDER BY timestamp DESC 
        LIMIT ?
        """
        return self.connection_manager.execute_query("E1", query, (function_name, limit))
        
    def get_slow_functions(self, threshold: float = 1.0) -> List[Dict[str, Any]]:
        """Get functions that are performing slowly (execution time > threshold)."""
        query = """
        SELECT function_name, 
               AVG(execution_time) as avg_time,
               COUNT(*) as call_count,
               SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as error_count
        FROM function_metrics
        GROUP BY function_name
        HAVING avg_time > ?
        ORDER BY avg_time DESC
        """
        return self.connection_manager.execute_query("E1", query, (threshold,))
        
    def clear_old_metrics(self, days: int = 30):
        """Clear metrics older than specified days."""
        query = """
        DELETE FROM function_metrics 
        WHERE timestamp < datetime('now', ?)
        """
        self.connection_manager.execute_write("E1", query, (f'-{days} days',))

# Global metrics instance
_metrics = PerformanceMetrics()

def measure_performance(threshold: Optional[float] = None):
    """
    Decorator to measure function performance.
    
    Args:
        threshold: Optional execution time threshold in seconds.
                If specified, logs a warning when execution time exceeds it.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            error_type = None
            success = True
            
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                error_type = type(e).__name__
                success = False
                raise
            finally:
                execution_time = time.time() - start_time
                
                if threshold and execution_time > threshold:
                    logger.warning(
                        f"Function {func.__name__} exceeded threshold "
                        f"({execution_time:.2f}s > {threshold:.2f}s)"
                    )
                
                _metrics.record_metric(
                    function_name=func.__name__,
                    execution_time=execution_time,
                    success=success,
                    error_type=error_type
                )
        return wrapper
    return decorator
