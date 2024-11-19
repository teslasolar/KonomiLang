import sqlite3
import json
from pathlib import Path

def check_version(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT m.version, m.script, v.applied_at, v.status 
            FROM schema_migrations m 
            JOIN schema_versions v ON m.version = v.version 
            WHERE v.status = 'success' 
            ORDER BY m.version DESC
            LIMIT 1;
        """)
        
        result = cursor.fetchone()
        if result:
            version, script, applied_at, status = result
            print(f"\nSchema Version Information for {db_path}:")
            print(f"Version: {version}")
            print(f"Status: {status}")
            print(f"Applied At: {applied_at}")
            print("\nScript Preview:")
            print("-" * 50)
            print(script[:200] + "..." if len(script) > 200 else script)
            return True
        else:
            print(f"\nNo successful migrations found in {db_path}")
            return False
            
    except Exception as e:
        print(f"Error checking version: {str(e)}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    db_path = Path("db_grid/A1/database.db")
    check_version(db_path)
