#!/usr/bin/env python3
"""
Command-line interface for backup and restore operations.
"""
import argparse
import sys
from database.backup_manager import BackupManager

def main():
    parser = argparse.ArgumentParser(description="Konomi Database Grid Backup Manager")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Backup command
    backup_parser = subparsers.add_parser("backup", help="Create a backup")
    backup_parser.add_argument(
        "--databases",
        nargs="*",
        help="List of database positions to backup (e.g., A1 B2). If not specified, backs up all databases."
    )
    
    # Restore command
    restore_parser = subparsers.add_parser("restore", help="Restore from backup")
    restore_parser.add_argument("backup_path", help="Path to backup directory")
    restore_parser.add_argument(
        "--databases",
        nargs="*",
        help="List of database positions to restore (e.g., A1 B2). If not specified, restores all databases in the backup."
    )
    
    # List backups command
    subparsers.add_parser("list", help="List available backups")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
        
    manager = BackupManager()
    
    try:
        if args.command == "backup":
            backup_path = manager.create_backup(args.databases)
            print(f"Backup created successfully at: {backup_path}")
            
        elif args.command == "restore":
            restored = manager.restore_backup(args.backup_path, args.databases)
            print(f"Successfully restored databases: {', '.join(restored)}")
            
        elif args.command == "list":
            backups = manager.list_backups()
            if not backups:
                print("No backups found.")
            else:
                print("\nAvailable backups:")
                for backup in backups:
                    print(f"\nBackup at: {backup['path']}")
                    print(f"Created: {backup['created_at']}")
                    print(f"Size: {backup['size']} bytes")
                    print(f"Status: {backup['status']}")
                    print(f"Databases: {', '.join(backup['databases'])}")
                    
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
