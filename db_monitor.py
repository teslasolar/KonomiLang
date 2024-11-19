import os
import sqlite3
import time
from datetime import datetime
import json

class DatabaseMonitor:
    def __init__(self, base_dir="db_grid"):
        self.base_dir = base_dir
        self.metrics_db = os.path.join(base_dir, "E1", "database.db")
        
    def check_connection(self, db_path):
        """Test database connection and return status."""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            conn.close()
            return True
        except sqlite3.Error:
            return False
            
    def get_db_size(self, db_path):
        """Get database file size in bytes."""
        try:
            return os.path.getsize(db_path)
        except OSError:
            return 0
            
    def check_table_integrity(self, db_path):
        """Check database table integrity."""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()[0]
            conn.close()
            return result == "ok"
        except sqlite3.Error:
            return False
            
    def get_table_counts(self, db_path):
        """Get record counts for all tables in database."""
        counts = {}
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get list of tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            # Count records in each table
            for (table_name,) in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                counts[table_name] = count
                
            conn.close()
            return counts
        except sqlite3.Error:
            return {}
            
    def store_metrics(self, position, metrics):
        """Store monitoring metrics in E1 database."""
        try:
            conn = sqlite3.connect(self.metrics_db)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO metrics (metric_type, value)
                VALUES (?, ?)
            """, (
                f"db_status_{position}",
                json.dumps(metrics)
            ))
            
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Error storing metrics: {str(e)}")
            
    def monitor_databases(self):
        """Monitor all databases in the grid."""
        results = {}
        
        for row in 'ABCDEFG':
            for col in range(1, 6):
                position = f"{row}{col}"
                db_path = os.path.join(self.base_dir, position, "database.db")
                
                metrics = {
                    "timestamp": datetime.now().isoformat(),
                    "connection_status": self.check_connection(db_path),
                    "size_bytes": self.get_db_size(db_path),
                    "integrity_check": self.check_table_integrity(db_path),
                    "table_counts": self.get_table_counts(db_path)
                }
                
                results[position] = metrics
                self.store_metrics(position, metrics)
                
        return results

def main():
    monitor = DatabaseMonitor()
    print("Starting database monitoring...")
    
    try:
        results = monitor.monitor_databases()
        total_dbs = len(results)
        healthy_dbs = sum(1 for metrics in results.values() if metrics["connection_status"] and metrics["integrity_check"])
        
        print(f"\nMonitoring complete:")
        print(f"Total databases monitored: {total_dbs}")
        print(f"Healthy databases: {healthy_dbs}/{total_dbs}")
        
        # Print detailed status for each database
        for position, metrics in results.items():
            status = "✓" if metrics["connection_status"] and metrics["integrity_check"] else "✗"
            size_mb = metrics["size_bytes"] / (1024 * 1024)
            print(f"\nDatabase {position} {status}")
            print(f"Size: {size_mb:.2f} MB")
            print(f"Tables: {len(metrics['table_counts'])}")
            print(f"Total Records: {sum(metrics['table_counts'].values())}")
            
    except Exception as e:
        print(f"Error during monitoring: {str(e)}")
        return False
        
    return healthy_dbs == total_dbs

if __name__ == "__main__":
    if main():
        print("\nSuccess: All databases are healthy!")
        exit(0)
    else:
        print("\nWarning: Some databases require attention.")
        exit(1)
