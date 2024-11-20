#!/usr/bin/env python3
"""
Unified CLI interface for Konomi operations.
"""
import argparse
import sys
import logging
from typing import Optional, List
from database.backup_manager import BackupManager
from database.connection_manager import DatabaseConnectionManager
from monitoring.service import MonitoringService
from generation.functions import DocumentationGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cli_operations.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class KonomiCLI:
    """Main CLI class for Konomi operations."""
    
    def __init__(self):
        self.parser = self._create_parser()
        self.backup_manager = BackupManager()
        self.connection_manager = DatabaseConnectionManager()
        self.monitor_service = MonitoringService()
        self.doc_generator = DocumentationGenerator()
        
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create and configure argument parser."""
        parser = argparse.ArgumentParser(
            description="Konomi CLI - Unified interface for all operations",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        subparsers = parser.add_subparsers(dest="command", help="Available commands")
        
        # Database commands
        db_parser = subparsers.add_parser("database", help="Database operations")
        db_subparsers = db_parser.add_subparsers(dest="db_command")
        
        # Initialize command
        init_parser = db_subparsers.add_parser("init", help="Initialize database grid")
        init_parser.add_argument("--force", action="store_true", help="Force reinitialization")
        
        # Populate command
        populate_parser = db_subparsers.add_parser("populate", help="Populate databases with initial data")
        populate_parser.add_argument("--positions", nargs="*", help="Specific database positions to populate")
        
        # Backup commands
        backup_parser = db_subparsers.add_parser("backup", help="Backup operations")
        backup_parser.add_argument("--databases", nargs="*", help="List of databases to backup")
        
        # Restore command
        restore_parser = db_subparsers.add_parser("restore", help="Restore from backup")
        restore_parser.add_argument("backup_path", help="Path to backup directory")
        restore_parser.add_argument("--databases", nargs="*", help="List of databases to restore")
        
        # List backups command
        db_subparsers.add_parser("list-backups", help="List available backups")
        
        # Monitor commands
        monitor_parser = subparsers.add_parser("monitor", help="Monitoring operations")
        monitor_subparsers = monitor_parser.add_subparsers(dest="monitor_command")
        
        # Start monitoring
        monitor_start = monitor_subparsers.add_parser("start", help="Start monitoring service")
        monitor_start.add_argument("--interval", type=int, default=300, help="Monitoring interval in seconds")
        
        # Stop monitoring
        monitor_subparsers.add_parser("stop", help="Stop monitoring service")
        
        # Status command
        monitor_subparsers.add_parser("status", help="Get current monitoring status")
        
        # Documentation commands
        docs_parser = subparsers.add_parser("docs", help="Documentation operations")
        docs_subparsers = docs_parser.add_subparsers(dest="docs_command")
        
        # Generate API docs
        docs_subparsers.add_parser("generate-api", help="Generate API documentation")
        
        # Generate function docs
        func_docs_parser = docs_subparsers.add_parser("generate-function", help="Generate function documentation")
        func_docs_parser.add_argument("file_path", help="Path to Python file")
        func_docs_parser.add_argument("--output", help="Output file path")
        
        return parser
        
    def handle_database_commands(self, args: argparse.Namespace) -> int:
        """Handle database-related commands."""
        try:
            if args.db_command == "init":
                from initialize_databases import main as init_main
                return 0 if init_main() else 1
                
            elif args.db_command == "populate":
                from populate_databases import main as populate_main
                return 0 if populate_main() else 1
                
            elif args.db_command == "backup":
                backup_path = self.backup_manager.create_backup(args.databases)
                if backup_path:
                    print(f"Backup created successfully at: {backup_path}")
                    return 0
                return 1
                
            elif args.db_command == "restore":
                restored = self.backup_manager.restore_backup(args.backup_path, args.databases)
                if restored:
                    print(f"Successfully restored databases: {', '.join(restored)}")
                    return 0
                return 1
                
            elif args.db_command == "list-backups":
                backups = self.backup_manager.list_backups()
                if backups:
                    for backup in backups:
                        print(f"\nBackup at: {backup['path']}")
                        print(f"Created: {backup['created_at']}")
                        print(f"Size: {backup['size']} bytes")
                        print(f"Databases: {', '.join(backup['databases'])}")
                else:
                    print("No backups found.")
                return 0
            
            logger.error(f"Unknown database command: {args.db_command}")
            return 1
                
        except Exception as e:
            logger.error(f"Database command failed: {str(e)}")
            return 1
            
    def handle_monitor_commands(self, args: argparse.Namespace) -> int:
        """Handle monitoring-related commands."""
        try:
            if args.monitor_command == "start":
                if hasattr(args, 'interval'):
                    self.monitor_service = MonitoringService(interval=args.interval)
                self.monitor_service.start()
                print("Monitoring service started successfully.")
                return 0
                
            elif args.monitor_command == "stop":
                self.monitor_service.stop()
                print("Monitoring service stopped successfully.")
                return 0
                
            elif args.monitor_command == "status":
                status = self.monitor_service.get_status()
                if status:
                    from db_monitor import format_monitoring_results
                    print(format_monitoring_results(status))
                else:
                    print("No monitoring data available.")
                return 0
            
            logger.error(f"Unknown monitor command: {args.monitor_command}")
            return 1
                
        except Exception as e:
            logger.error(f"Monitor command failed: {str(e)}")
            return 1
            
    def handle_docs_commands(self, args: argparse.Namespace) -> int:
        """Handle documentation-related commands."""
        try:
            if args.docs_command == "generate-api":
                from app import app, doc_generator
                import asyncio
                endpoints = doc_generator.discover_endpoints(app)
                asyncio.run(doc_generator.generate_api_docs(endpoints))
                print("API documentation generated successfully.")
                return 0
                
            elif args.docs_command == "generate-function":
                import asyncio
                content = asyncio.run(self.doc_generator.generate_function_docs(
                    args.file_path,
                    args.output
                ))
                if args.output:
                    print(f"Function documentation generated and saved to: {args.output}")
                else:
                    print("\nGenerated Documentation:")
                    print("=" * 40)
                    print(content)
                return 0
            
            logger.error(f"Unknown docs command: {args.docs_command}")
            return 1
                
        except Exception as e:
            logger.error(f"Documentation command failed: {str(e)}")
            return 1
            
    def execute(self) -> int:
        """Execute CLI command."""
        args = self.parser.parse_args()
        
        if not args.command:
            self.parser.print_help()
            return 1
            
        try:
            if args.command == "database":
                return self.handle_database_commands(args)
            elif args.command == "monitor":
                return self.handle_monitor_commands(args)
            elif args.command == "docs":
                return self.handle_docs_commands(args)
                
        except Exception as e:
            logger.error(f"Command execution failed: {str(e)}")
            return 1
            
        return 0

def main():
    cli = KonomiCLI()
    sys.exit(cli.execute())

if __name__ == "__main__":
    main()
