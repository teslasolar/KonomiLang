import os
import sqlite3
import string
import sys

def create_grid_structure():
    # Create main directory for the database grid
    base_dir = "db_grid"
    print(f"Creating base directory: {base_dir}")
    os.makedirs(base_dir, exist_ok=True)
    
    # Create 5x5 grid of directories and databases
    rows = list(string.ascii_uppercase[:5])  # A through E
    cols = range(1, 6)  # 1 through 5
    
    created_dbs = []
    
    for row in rows:
        for col in cols:
            try:
                # Create directory
                dir_name = f"{base_dir}/{row}{col}"
                print(f"Creating directory: {dir_name}")
                os.makedirs(dir_name, exist_ok=True)
                
                # Create and initialize database
                db_path = f"{dir_name}/database.db"
                print(f"Creating database: {db_path}")
                conn = sqlite3.connect(db_path)
                
                # Create a simple test table to verify database initialization
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS grid_info (
                        id INTEGER PRIMARY KEY,
                        position TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Insert grid position information
                cursor.execute('INSERT INTO grid_info (position) VALUES (?)', (f"{row}{col}",))
                
                conn.commit()
                conn.close()
                
                created_dbs.append(f"{row}{col}")
                print(f"Successfully created database at position {row}{col}")
            except Exception as e:
                print(f"Error creating database at position {row}{col}: {str(e)}", file=sys.stderr)
    
    return created_dbs

if __name__ == "__main__":
    print("Creating 5x5 grid of SQLite databases...")
    created_dbs = create_grid_structure()
    print(f"Successfully created databases in positions: {', '.join(created_dbs)}")
    
    # Verify the structure
    base_dir = "db_grid"
    if os.path.exists(base_dir):
        print("\nDirectory structure:")
        for root, dirs, files in os.walk(base_dir):
            level = root.replace(base_dir, '').count(os.sep)
            indent = ' ' * 4 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                print(f"{subindent}{f}")
