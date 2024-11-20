"""
Base Router Module

Provides base classes and utilities for consistent route handling
across the application.
"""
from typing import Any, Dict, Optional, Callable
from flask import Blueprint, jsonify, Response
import logging

logger = logging.getLogger(__name__)

class APIRouter:
    """Base class for API route handlers with consistent error handling and responses."""
    
    def __init__(self, blueprint: Blueprint):
        self.blueprint = blueprint
        self.logger = logger.getChild(self.__class__.__name__)
    
    def json_response(self, data: Dict[str, Any], status_code: int = 200) -> Response:
        """Create a consistent JSON response."""
        return jsonify(data), status_code
    
    def error_response(self, message: str, status_code: int = 400) -> Response:
        """Create a consistent error response."""
        return self.json_response({'success': False, 'error': message}, status_code)
    
    def success_response(self, data: Optional[Dict[str, Any]] = None) -> Response:
        """Create a consistent success response."""
        response_data = {'success': True}
        if data:
            response_data.update(data)
        return self.json_response(response_data)
    
    def route(self, rule: str, **options: Any) -> Callable:
        """Route decorator with error handling."""
        def decorator(f: Callable) -> Callable:
            @self.blueprint.route(rule, **options)
            def wrapped(*args: Any, **kwargs: Any) -> Response:
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    self.logger.error(f"Error in route {rule}: {str(e)}")
                    return self.error_response(str(e), 500)
            return wrapped
        return decorator
