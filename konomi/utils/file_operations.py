"""
File System Operation Utilities

This module provides utilities for safe file system operations.
"""
import os
from typing import List, Optional
from ..errors import RuntimeError

def safe_list_directory(path: Optional[str] = None) -> str:
    """
    Safely list contents of a directory.
    
    Args:
        path: Directory path (default: current directory)
        
    Returns:
        Formatted string of directory contents
        
    Raises:
        RuntimeError: If directory operation fails
    """
    try:
        path = "." if path is None else path
        if not os.path.exists(path):
            raise RuntimeError(f"Directory not found: {path}")
        items = os.listdir(path)
        return "\n".join([
            f"{'[DIR] ' if os.path.isdir(os.path.join(path, item)) else '[FILE] '}{item}"
            for item in sorted(items)
        ])
    except Exception as e:
        raise RuntimeError(f"File System Error: {str(e)}")

def safe_create_directory(path: str) -> str:
    """
    Safely create a directory.
    
    Args:
        path: Directory path to create
        
    Returns:
        Success message
        
    Raises:
        RuntimeError: If directory creation fails
    """
    try:
        os.makedirs(path, exist_ok=True)
        return f"Directory created: {path}"
    except Exception as e:
        raise RuntimeError(f"File System Error: {str(e)}")

def safe_remove_directory(path: str) -> str:
    """
    Safely remove a directory.
    
    Args:
        path: Directory path to remove
        
    Returns:
        Success message
        
    Raises:
        RuntimeError: If directory removal fails
    """
    try:
        if not os.path.exists(path):
            raise RuntimeError(f"Directory not found: {path}")
        if not os.path.isdir(path):
            raise RuntimeError(f"Not a directory: {path}")
        os.rmdir(path)
        return f"Directory removed: {path}"
    except Exception as e:
        raise RuntimeError(f"File System Error: {str(e)}")
