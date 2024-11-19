"""
Error Handling Utilities

This module provides error handling utilities and helper functions for the Konomi language.
"""
from typing import Optional, Any, Dict
from ..errors import RuntimeError

def validate_type(value: Any, expected_type: type, var_name: str) -> None:
    """
    Validate that a value matches the expected type.
    
    Args:
        value: The value to validate
        expected_type: The expected type
        var_name: Name of the variable for error messages
        
    Raises:
        RuntimeError: If type validation fails
    """
    if not isinstance(value, expected_type):
        raise RuntimeError(f"Expected {var_name} to be of type {expected_type.__name__}, got {type(value).__name__}")

def validate_operation(left: Any, right: Any, op: str) -> None:
    """
    Validate that an operation can be performed between two values.
    
    Args:
        left: Left operand
        right: Right operand
        op: Operation symbol
        
    Raises:
        RuntimeError: If operation validation fails
    """
    valid_ops = {
        '+': (str, (int, float)),
        '-': ((int, float),),
        '*': ((int, float),),
        '/': ((int, float),)
    }
    
    if op in valid_ops:
        valid_types = valid_ops[op]
        for types in valid_types:
            if isinstance(left, types) and isinstance(right, types):
                return
        raise RuntimeError(f"Invalid operation {op} between types {type(left).__name__} and {type(right).__name__}")

def safe_execute(func: callable, error_msg: str, *args, **kwargs) -> Any:
    """
    Safely execute a function with error handling.
    
    Args:
        func: Function to execute
        error_msg: Error message prefix
        *args: Positional arguments
        **kwargs: Keyword arguments
        
    Returns:
        The function result
        
    Raises:
        RuntimeError: If function execution fails
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        raise RuntimeError(f"{error_msg}: {str(e)}")
