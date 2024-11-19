import os
import sqlite3
import sys

def verify_grid_structure():
    base_dir = "db_grid"
    if not os.path.exists(base_dir):
        print("Error: db_grid directory not found!")
        return False
    
    success = True
    total_dbs = 0
    
    for row in 'ABCDE':
        for col in range(1, 6):
            position = f"{row}{col}"
            db_path = f"{base_dir}/{position}/database.db"
            
            if not os.path.exists(db_path):
                print(f"Error: Database not found at {db_path}")
                success = False
                continue
                
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Verify table exists
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name='grid_info';
                """)
                if not cursor.fetchone():
                    print(f"Error: grid_info table not found in database at {position}")
                    success = False
                    continue
                
                # Verify position data
                cursor.execute("SELECT position FROM grid_info")
                stored_position = cursor.fetchone()
                if not stored_position or stored_position[0] != position:
                    print(f"Error: Incorrect position data in database at {position}")
                    success = False
                else:
                    total_dbs += 1
                
                conn.close()
                
            except sqlite3.Error as e:
                print(f"Error accessing database at {position}: {str(e)}")
                success = False
    
    print(f"\nVerification complete:")
    print(f"Total valid databases found: {total_dbs}/25")
    return success and total_dbs == 25

if __name__ == "__main__":
    print("Verifying 5x5 grid of SQLite databases...")
    if verify_grid_structure():
        print("Success: All databases are properly initialized!")
        sys.exit(0)
    else:
        print("Error: Some databases are not properly initialized.")
        sys.exit(1)
