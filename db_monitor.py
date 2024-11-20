import os
import sqlite3
import time
from datetime import datetime
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('monitoring_operations.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class DatabaseMetrics:
    """Database monitoring metrics."""
    timestamp: str
    connection_status: bool
    size_bytes: int
    integrity_check: bool
    table_counts: Dict[str, int]

@dataclass
class DatabaseInfo:
    """Database information container."""
    position: str
    path: Path
    metrics: Optional[DatabaseMetrics] = None

class DatabaseMonitor:
    """Monitors database health and performance."""
    
    def __init__(self, base_dir: str = "db_grid"):
        """Initialize DatabaseMonitor with base directory."""
        self.base_dir = Path(base_dir)
        self.metrics_db = self.base_dir / "E1" / "database.db"
        self.logger = logger.getChild(self.__class__.__name__)
        
    def _get_connection(self, db_path: Path) -> Optional[sqlite3.Connection]:
        """Get a database connection with proper error handling."""
        try:
            return sqlite3.connect(db_path)
        except sqlite3.Error as e:
            self.logger.error(f"Failed to connect to database {db_path}: {str(e)}")
            return None

    def _execute_query(self, db_path: Path, query: str, params: tuple = ()) -> Optional[sqlite3.Cursor]:
        """Execute a database query with proper connection and parameter handling."""
        conn = None
        try:
            conn = self._get_connection(db_path)
            if not conn:
                return None

            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor
        except sqlite3.Error as e:
            self.logger.error(f"Database query failed for {db_path}: {str(e)}")
            if conn:
                conn.close()
            return None

    def check_connection(self, db_path: Path) -> bool:
        """Test database connection and return status."""
        try:
            cursor = self._execute_query(db_path, "SELECT 1")
            if cursor:
                cursor.connection.close()
                return True
            return False
        except Exception as e:
            self.logger.error(f"Connection check failed for {db_path}: {str(e)}")
            return False
            
    def get_db_size(self, db_path: Path) -> int:
        """Get database file size in bytes."""
        try:
            return db_path.stat().st_size
        except OSError as e:
            self.logger.error(f"Failed to get size for {db_path}: {str(e)}")
            return 0
            
    def check_table_integrity(self, db_path: Path) -> bool:
        """Check database table integrity."""
        try:
            cursor = self._execute_query(db_path, "PRAGMA integrity_check")
            if cursor:
                result = cursor.fetchone()[0]
                cursor.connection.close()
                return result == "ok"
            return False
        except Exception as e:
            self.logger.error(f"Integrity check failed for {db_path}: {str(e)}")
            return False
            
    def get_table_counts(self, db_path: Path) -> Dict[str, int]:
        """Get record counts for all tables in database."""
        counts: Dict[str, int] = {}
        try:
            cursor = self._execute_query(db_path, "SELECT name FROM sqlite_master WHERE type='table'")
            if not cursor:
                return counts

            tables = cursor.fetchall()
            
            # Count records in each table
            for (table_name,) in tables:
                count_cursor = self._execute_query(db_path, f"SELECT COUNT(*) FROM {table_name}")
                if count_cursor:
                    count = count_cursor.fetchone()[0]
                    counts[table_name] = count
                    count_cursor.connection.close()
            
            cursor.connection.close()
            return counts
        except Exception as e:
            self.logger.error(f"Failed to get table counts for {db_path}: {str(e)}")
            return counts
            
    def _initialize_metrics_table(self) -> bool:
        """Initialize metrics table in E1 database."""
        try:
            conn = sqlite3.connect(self.metrics_db)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_type TEXT NOT NULL,
                    value TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize metrics table: {str(e)}")
            return False

    def _serialize_metrics(self, metrics: DatabaseMetrics) -> str:
        """Serialize metrics data to JSON string."""
        return json.dumps({
            "timestamp": metrics.timestamp,
            "connection_status": metrics.connection_status,
            "size_bytes": metrics.size_bytes,
            "integrity_check": metrics.integrity_check,
            "table_counts": metrics.table_counts
        })

    def _get_metrics_connection(self) -> Optional[sqlite3.Connection]:
        """Get a dedicated connection to the metrics database."""
        try:
            if not self.metrics_db.parent.exists():
                self.metrics_db.parent.mkdir(parents=True, exist_ok=True)
            return sqlite3.connect(str(self.metrics_db))
        except Exception as e:
            self.logger.error(f"Failed to connect to metrics database: {str(e)}")
            return None

    def store_metrics(self, db_info: DatabaseInfo) -> bool:
        """Store monitoring metrics in E1 database."""
        if not db_info.metrics:
            self.logger.warning(f"No metrics available for database {db_info.position}")
            return False

        conn = None
        try:
            # Get dedicated connection for metrics storage
            conn = self._get_metrics_connection()
            if not conn:
                return False

            # Initialize metrics table if needed
            if not self._initialize_metrics_table():
                return False

            # Prepare metric data
            metric_type = f"db_status_{db_info.position}"
            metric_value = self._serialize_metrics(db_info.metrics)

            # Execute insert with proper parameter binding
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO metrics (metric_type, value) VALUES (?, ?)",
                (metric_type, metric_value)
            )
            
            conn.commit()
            self.logger.info(f"Successfully stored metrics for database {db_info.position}")
            return True

        except sqlite3.Error as e:
            self.logger.error(f"Database error storing metrics for {db_info.position}: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error storing metrics for {db_info.position}: {str(e)}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as e:
                    self.logger.error(f"Error closing metrics database connection: {str(e)}")
            
    def collect_database_metrics(self, db_info: DatabaseInfo) -> DatabaseMetrics:
        """Collect all metrics for a single database."""
        return DatabaseMetrics(
            timestamp=datetime.now().isoformat(),
            connection_status=self.check_connection(db_info.path),
            size_bytes=self.get_db_size(db_info.path),
            integrity_check=self.check_table_integrity(db_info.path),
            table_counts=self.get_table_counts(db_info.path)
        )

    def get_database_list(self) -> List[DatabaseInfo]:
        """Get list of all databases in the grid."""
        databases = []
        for row in 'ABCDEFG':
            for col in range(1, 6):
                position = f"{row}{col}"
                db_path = self.base_dir / position / "database.db"
                databases.append(DatabaseInfo(position=position, path=db_path))
        return databases

    def monitor_databases(self) -> Dict[str, DatabaseMetrics]:
        """Monitor all databases in the grid."""
        results: Dict[str, DatabaseMetrics] = {}
        
        try:
            databases = self.get_database_list()
            
            for db_info in databases:
                try:
                    metrics = self.collect_database_metrics(db_info)
                    db_info.metrics = metrics
                    results[db_info.position] = metrics
                    
                    if not self.store_metrics(db_info):
                        self.logger.warning(f"Failed to store metrics for database {db_info.position}")
                        
                except Exception as e:
                    self.logger.error(f"Error monitoring database {db_info.position}: {str(e)}")
                    continue
                    
            return results
        except Exception as e:
            self.logger.error(f"Critical error during database monitoring: {str(e)}")
            return results

def format_monitoring_results(results: Dict[str, DatabaseMetrics]) -> str:
    """Format monitoring results for display."""
    output = []
    total_dbs = len(results)
    healthy_dbs = sum(
        1 for metrics in results.values() 
        if metrics.connection_status and metrics.integrity_check
    )
    
    output.append("\nMonitoring Summary:")
    output.append(f"Total databases monitored: {total_dbs}")
    output.append(f"Healthy databases: {healthy_dbs}/{total_dbs}")
    
    output.append("\nDetailed Status:")
    for position, metrics in sorted(results.items()):
        status = "✓" if metrics.connection_status and metrics.integrity_check else "✗"
        size_mb = metrics.size_bytes / (1024 * 1024)
        total_records = sum(metrics.table_counts.values())
        
        output.extend([
            f"\nDatabase {position} {status}",
            f"Size: {size_mb:.2f} MB",
            f"Tables: {len(metrics.table_counts)}",
            f"Total Records: {total_records}"
        ])
    
    return "\n".join(output)

def main() -> bool:
    """Main execution function."""
    monitor = DatabaseMonitor()
    logger.info("Starting database monitoring...")
    
    try:
        results = monitor.monitor_databases()
        
        if not results:
            logger.error("No monitoring results obtained")
            return False
            
        print(format_monitoring_results(results))
        
        healthy_count = sum(
            1 for metrics in results.values() 
            if metrics.connection_status and metrics.integrity_check
        )
        return healthy_count == len(results)
        
    except Exception as e:
        logger.error(f"Error during monitoring: {str(e)}")
        return False

if __name__ == "__main__":
    if main():
        logger.info("Success: All databases are healthy!")
        exit(0)
    else:
        logger.warning("Warning: Some databases require attention.")
        exit(1)
