#!/usr/bin/env python3
"""
Command-line interface for backup and restore operations.
"""
import argparse
import sys
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from database.backup_manager import BackupManager
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backup_operations.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class BackupConfig:
    """Configuration for backup operations."""
    databases: Optional[List[str]] = None
    backup_path: Optional[str] = None

class CommandParser:
    """Handles command-line argument parsing."""
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Konomi Database Grid Backup Manager")
        self._setup_parsers()

    def _setup_parsers(self) -> None:
        """Set up command-line argument parsers."""
        subparsers = self.parser.add_subparsers(dest="command", help="Command to execute")
        
        # Backup command
        self._setup_backup_parser(subparsers)
        
        # Restore command
        self._setup_restore_parser(subparsers)
        
        # List backups command
        subparsers.add_parser("list", help="List available backups")

    def _setup_backup_parser(self, subparsers: argparse._SubParsersAction) -> None:
        """Set up backup command parser."""
        backup_parser = subparsers.add_parser("backup", help="Create a backup")
        backup_parser.add_argument(
            "--databases",
            nargs="*",
            help="List of database positions to backup (e.g., A1 B2). If not specified, backs up all databases."
        )

    def _setup_restore_parser(self, subparsers: argparse._SubParsersAction) -> None:
        """Set up restore command parser."""
        restore_parser = subparsers.add_parser("restore", help="Restore from backup")
        restore_parser.add_argument("backup_path", help="Path to backup directory")
        restore_parser.add_argument(
            "--databases",
            nargs="*",
            help="List of database positions to restore (e.g., A1 B2). If not specified, restores all databases in the backup."
        )

    def parse_args(self) -> argparse.Namespace:
        """Parse command-line arguments."""
        args = self.parser.parse_args()
        if not args.command:
            self.parser.print_help()
            sys.exit(1)
        return args

class BackupCLI:
    """Handles backup CLI operations."""
    def __init__(self):
        self.manager = BackupManager()
        self.parser = CommandParser()

    def create_backup(self, config: BackupConfig) -> str:
        """Create a backup of specified databases."""
        try:
            backup_path = self.manager.create_backup(config.databases)
            logger.info(f"Backup created successfully at: {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"Backup creation failed: {str(e)}")
            raise

    def restore_backup(self, config: BackupConfig) -> List[str]:
        """Restore databases from a backup."""
        try:
            restored = self.manager.restore_backup(config.backup_path, config.databases)
            logger.info(f"Successfully restored databases: {', '.join(restored)}")
            return restored
        except Exception as e:
            logger.error(f"Backup restoration failed: {str(e)}")
            raise

    def format_backup_info(self, backup: Dict[str, Any]) -> str:
        """Format backup information for display."""
        return (
            f"\nBackup at: {backup['path']}\n"
            f"Created: {backup['created_at']}\n"
            f"Size: {backup['size']} bytes\n"
            f"Status: {backup['status']}\n"
            f"Databases: {', '.join(backup['databases'])}"
        )

    def list_backups(self) -> None:
        """List all available backups."""
        try:
            backups = self.manager.list_backups()
            if not backups:
                print("No backups found.")
                return

            print("\nAvailable backups:")
            for backup in backups:
                print(self.format_backup_info(backup))
        except Exception as e:
            logger.error(f"Failed to list backups: {str(e)}")
            raise

    def execute(self) -> int:
        """Execute CLI command."""
        try:
            args = self.parser.parse_args()
            config = BackupConfig(
                databases=args.databases if hasattr(args, 'databases') else None,
                backup_path=args.backup_path if hasattr(args, 'backup_path') else None
            )

            if args.command == "backup":
                self.create_backup(config)
            elif args.command == "restore":
                self.restore_backup(config)
            elif args.command == "list":
                self.list_backups()

            return 0
        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            return 1

def main():
    cli = BackupCLI()
    sys.exit(cli.execute())

if __name__ == "__main__":
    main()
