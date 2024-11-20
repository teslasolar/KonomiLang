"""
Decorators for HTML component API documentation and dependency tracking
"""
from functools import wraps
from typing import Optional, List, Dict, Any
import inspect

class ComponentDependency:
    """Track component dependencies and version compatibility."""
    def __init__(self, component: str, version: str):
        self.component = component
        self.version = version

def api_doc(description: str, 
            inputs: Dict[str, str] = None,
            outputs: str = None,
            example: str = None,
            dependencies: List[ComponentDependency] = None):
    """
    Decorator to document component APIs and track dependencies.
    
    Args:
        description: Brief description of the component/method
        inputs: Dictionary of parameter names and their descriptions
        outputs: Description of the return value
        example: Usage example code
        dependencies: List of component dependencies
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
            
        # Store API documentation
        wrapper.__api_doc__ = {
            'description': description,
            'inputs': inputs or {},
            'outputs': outputs,
            'example': example,
            'dependencies': dependencies or []
        }
        
        # Store signature for validation
        wrapper.__signature__ = inspect.signature(func)
        return wrapper
    return decorator

def depends_on(*components: str, min_version: Optional[str] = None):
    """
    Decorator to specify component dependencies.
    
    Args:
        *components: Component names this component depends on
        min_version: Minimum required version
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Future: Add version compatibility checks here
            return func(*args, **kwargs)
            
        wrapper.__dependencies__ = [
            ComponentDependency(comp, min_version) for comp in components
        ]
        return wrapper
    return decorator
