"""
Backup manager for the Konomi database grid system.
Handles backup and restore operations for all databases.
"""
import os
import sqlite3
import shutil
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
from database.connection_manager import DatabaseConnectionManager

class BackupManager:
    def __init__(self, base_dir: str = "db_grid", backup_dir: str = "backups"):
        self.base_dir = base_dir
        self.backup_dir = backup_dir
        self.connection_manager = DatabaseConnectionManager()
        
        # Create backup directory if it doesn't exist
        os.makedirs(backup_dir, exist_ok=True)
        
    def _calculate_checksum(self, file_path: str) -> str:
        """Calculate SHA-256 checksum of a file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
        
    def _create_backup_metadata(self, backup_path: str, databases: List[str]) -> Dict:
        """Create metadata for backup."""
        total_size = sum(os.path.getsize(os.path.join(backup_path, f"{db}.db")) 
                        for db in databases)
        checksums = {db: self._calculate_checksum(os.path.join(backup_path, f"{db}.db"))
                    for db in databases}
                    
        return {
            "timestamp": datetime.now().isoformat(),
            "databases": databases,
            "total_size": total_size,
            "checksums": checksums,
            "version": "1.0"
        }
        
    def _store_backup_record(self, backup_path: str, size: int):
        """Store backup record in E4 database."""
        query = """
        INSERT INTO backups (backup_path, size, status, created_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """
        self.connection_manager.execute_write("E4", query, (backup_path, size, "completed"))
        
    def create_backup(self, positions: Optional[List[str]] = None) -> str:
        """
        Create a backup of specified databases or all databases.
        
        Args:
            positions: List of database positions to backup (e.g., ['A1', 'B2']).
                      If None, backs up all databases.
                      
        Returns:
            Path to the backup directory
        """
        # Default to all positions if none specified
        if positions is None:
            positions = []
            for row in 'ABCDEFG':
                for col in range(1, 6):
                    positions.append(f"{row}{col}")
                    
        # Create timestamped backup directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(self.backup_dir, f"backup_{timestamp}")
        os.makedirs(backup_path)
        
        successful_backups = []
        
        for pos in positions:
            try:
                db_path = os.path.join(self.base_dir, pos, "database.db")
                backup_db_path = os.path.join(backup_path, f"{pos}.db")
                
                # Ensure source database exists
                if not os.path.exists(db_path):
                    print(f"Warning: Database {pos} not found, skipping...")
                    continue
                    
                # Create backup copy
                shutil.copy2(db_path, backup_db_path)
                
                # Verify backup integrity
                if self._verify_backup(db_path, backup_db_path):
                    successful_backups.append(pos)
                else:
                    print(f"Warning: Backup verification failed for {pos}")
                    os.remove(backup_db_path)
                    
            except Exception as e:
                print(f"Error backing up database {pos}: {str(e)}")
                continue
                
        # Create and save backup metadata
        if successful_backups:
            metadata = self._create_backup_metadata(backup_path, successful_backups)
            with open(os.path.join(backup_path, "metadata.json"), "w") as f:
                json.dump(metadata, f, indent=2)
                
            # Store backup record
            total_size = metadata["total_size"]
            self._store_backup_record(backup_path, total_size)
            
            return backup_path
        else:
            # Clean up if no successful backups
            shutil.rmtree(backup_path)
            raise RuntimeError("No databases were successfully backed up")
            
    def _verify_backup(self, source_path: str, backup_path: str) -> bool:
        """Verify backup integrity by comparing checksums."""
        return self._calculate_checksum(source_path) == self._calculate_checksum(backup_path)
        
    def restore_backup(self, backup_path: str, positions: Optional[List[str]] = None) -> List[str]:
        """
        Restore databases from a backup.
        
        Args:
            backup_path: Path to backup directory
            positions: List of database positions to restore.
                      If None, restores all databases in the backup.
                      
        Returns:
            List of successfully restored database positions
        """
        # Verify backup exists
        if not os.path.exists(backup_path):
            raise ValueError(f"Backup not found: {backup_path}")
            
        # Load backup metadata
        metadata_path = os.path.join(backup_path, "metadata.json")
        if not os.path.exists(metadata_path):
            raise ValueError("Invalid backup: metadata.json not found")
            
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
            
        # Determine which databases to restore
        available_dbs = metadata["databases"]
        if positions is None:
            positions = available_dbs
        else:
            # Verify requested positions exist in backup
            invalid_positions = set(positions) - set(available_dbs)
            if invalid_positions:
                raise ValueError(f"Databases not found in backup: {invalid_positions}")
                
        restored_dbs = []
        
        for pos in positions:
            try:
                backup_db_path = os.path.join(backup_path, f"{pos}.db")
                target_db_path = os.path.join(self.base_dir, pos, "database.db")
                
                # Verify backup file integrity
                if not self._verify_backup(backup_db_path, backup_db_path):
                    print(f"Warning: Backup verification failed for {pos}")
                    continue
                    
                # Create backup of current database before restoring
                if os.path.exists(target_db_path):
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    shutil.copy2(target_db_path, 
                               f"{target_db_path}.pre_restore_{timestamp}")
                    
                # Restore database
                shutil.copy2(backup_db_path, target_db_path)
                
                # Verify restoration
                if self._verify_backup(backup_db_path, target_db_path):
                    restored_dbs.append(pos)
                else:
                    print(f"Warning: Restoration verification failed for {pos}")
                    
            except Exception as e:
                print(f"Error restoring database {pos}: {str(e)}")
                continue
                
        return restored_dbs
        
    def list_backups(self) -> List[Dict]:
        """List all available backups with their metadata."""
        query = """
        SELECT backup_path, size, status, created_at
        FROM backups
        ORDER BY created_at DESC
        """
        backups = self.connection_manager.execute_query("E4", query)
        
        result = []
        for backup in backups:
            metadata_path = os.path.join(backup['backup_path'], "metadata.json")
            if os.path.exists(metadata_path):
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                result.append({
                    "path": backup['backup_path'],
                    "size": backup['size'],
                    "status": backup['status'],
                    "created_at": backup['created_at'],
                    "databases": metadata['databases'],
                    "version": metadata.get('version', '1.0')
                })
                
        return result
