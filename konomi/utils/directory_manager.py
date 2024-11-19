"""
Dynamic Directory Structure Manager for KonomiLang
Handles creation, validation, and management of directory structures
"""
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
import shutil
import json
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DirectoryManager:
    def __init__(self, base_path: Union[str, Path] = "."):
        self.base_path = Path(base_path).resolve()
        self._history: List[Dict[str, Any]] = []
        self._setup_logging()

    def _setup_logging(self):
        """Configure logging for directory operations"""
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler = logging.FileHandler('directory_operations.log')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    def validate_template(self, template: Dict[str, Any]) -> bool:
        """
        Validate directory structure template
        
        Args:
            template: Dictionary representing directory structure
            
        Returns:
            bool: True if template is valid, False otherwise
        """
        def validate_node(node: Any) -> bool:
            if isinstance(node, dict):
                return all(isinstance(key, str) and validate_node(value) 
                         for key, value in node.items())
            return isinstance(node, (str, type(None)))

        try:
            return validate_node(template)
        except Exception as e:
            logger.error(f"Template validation failed: {str(e)}")
            return False

    def create_structure(self, template: Dict[str, Any], path: Optional[Union[str, Path]] = None) -> bool:
        """
        Create directory structure from template
        
        Args:
            template: Dictionary representing directory structure
            path: Optional custom path, defaults to base_path
            
        Returns:
            bool: True if structure was created successfully
        """
        current_path = Path(path) if path else self.base_path
        operation_time = datetime.now()

        def create_node(structure: Dict, current: Path) -> None:
            for name, content in structure.items():
                node_path = current / name
                
                try:
                    if isinstance(content, dict):
                        node_path.mkdir(exist_ok=True)
                        create_node(content, node_path)
                    else:
                        node_path.parent.mkdir(parents=True, exist_ok=True)
                        if content is not None:
                            with open(node_path, 'w') as f:
                                f.write(str(content))
                except Exception as e:
                    logger.error(f"Failed to create {node_path}: {str(e)}")
                    raise

        try:
            if not self.validate_template(template):
                raise ValueError("Invalid template format")

            create_node(template, current_path)
            
            # Record operation in history
            self._history.append({
                'operation': 'create_structure',
                'template': template,
                'path': str(current_path),
                'timestamp': operation_time
            })
            
            logger.info(f"Created directory structure at {current_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to create directory structure: {str(e)}")
            return False

    def list_directory(self, path: Optional[Union[str, Path]] = None) -> List[Dict[str, Any]]:
        """
        List contents of a directory with metadata
        
        Args:
            path: Optional path to list, defaults to base_path
            
        Returns:
            List of dictionaries containing file/directory information
        """
        target_path = Path(path) if path else self.base_path
        
        try:
            contents = []
            for item in target_path.iterdir():
                info = {
                    'name': item.name,
                    'type': 'directory' if item.is_dir() else 'file',
                    'path': str(item.relative_to(self.base_path)),
                    'modified': datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                }
                if not item.is_dir():
                    info['size'] = item.stat().st_size
                contents.append(info)
            
            logger.info(f"Listed directory contents at {target_path}")
            return contents
        except Exception as e:
            logger.error(f"Failed to list directory {target_path}: {str(e)}")
            return []

    def remove_structure(self, path: Union[str, Path]) -> bool:
        """
        Safely remove directory structure
        
        Args:
            path: Path to remove
            
        Returns:
            bool: True if structure was removed successfully
        """
        target_path = Path(path)
        operation_time = datetime.now()

        try:
            if not target_path.exists():
                logger.warning(f"Path does not exist: {target_path}")
                return False

            if target_path.is_file():
                target_path.unlink()
            else:
                shutil.rmtree(target_path)

            # Record operation in history
            self._history.append({
                'operation': 'remove_structure',
                'path': str(target_path),
                'timestamp': operation_time
            })

            logger.info(f"Removed structure at {target_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to remove structure at {target_path}: {str(e)}")
            return False

    def get_structure(self, path: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
        """
        Get current directory structure as a template
        
        Args:
            path: Optional path to start from, defaults to base_path
            
        Returns:
            Dictionary representing current directory structure
        """
        current_path = Path(path) if path else self.base_path

        def build_structure(current: Path) -> Union[Dict[str, Any], None]:
            if current.is_file():
                try:
                    with open(current, 'r') as f:
                        return f.read()
                except:
                    return None

            structure = {}
            try:
                for item in current.iterdir():
                    structure[item.name] = build_structure(item)
                return structure
            except Exception as e:
                logger.error(f"Failed to build structure for {current}: {str(e)}")
                return {}

        try:
            return build_structure(current_path) or {}
        except Exception as e:
            logger.error(f"Failed to get structure: {str(e)}")
            return {}

    def export_template(self, path: Union[str, Path]) -> bool:
        """
        Export current directory structure as a template file
        
        Args:
            path: Path to save template file
            
        Returns:
            bool: True if template was exported successfully
        """
        try:
            structure = self.get_structure()
            with open(path, 'w') as f:
                json.dump(structure, f, indent=2)
            logger.info(f"Exported template to {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to export template: {str(e)}")
            return False

    def import_template(self, path: Union[str, Path]) -> Optional[Dict[str, Any]]:
        """
        Import directory structure template from file
        
        Args:
            path: Path to template file
            
        Returns:
            Imported template dictionary or None if import failed
        """
        try:
            with open(path, 'r') as f:
                template = json.load(f)
            if self.validate_template(template):
                logger.info(f"Imported template from {path}")
                return template
            logger.error("Invalid template format in imported file")
            return None
        except Exception as e:
            logger.error(f"Failed to import template: {str(e)}")
            return None

    def get_history(self) -> List[Dict[str, Any]]:
        """Get operation history"""
        return self._history.copy()

    def clear_history(self) -> None:
        """Clear operation history"""
        self._history.clear()
        logger.info("Cleared operation history")
