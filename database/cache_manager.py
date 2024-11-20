"""
Cache manager for database operations.
Provides function-level caching with TTL and size limits.
"""
import time
import threading
from typing import Any, Dict, Optional, Tuple, Callable
from functools import wraps
from collections import OrderedDict

class DatabaseCache:
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        self.max_size = max_size
        self.ttl = ttl
        self._cache: OrderedDict[str, Tuple[Any, float]] = OrderedDict()
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired."""
        with self._lock:
            if key in self._cache:
                value, timestamp = self._cache[key]
                if time.time() - timestamp <= self.ttl:
                    # Move to end to mark as recently used
                    self._cache.move_to_end(key)
                    return value
                # Remove if expired
                del self._cache[key]
            return None

    def set(self, key: str, value: Any):
        """Set value in cache with current timestamp."""
        with self._lock:
            # Remove oldest if at max size
            if len(self._cache) >= self.max_size:
                self._cache.popitem(last=False)
            self._cache[key] = (value, time.time())

    def invalidate(self, key: str):
        """Remove specific key from cache."""
        with self._lock:
            self._cache.pop(key, None)

    def clear(self):
        """Clear entire cache."""
        with self._lock:
            self._cache.clear()

def cache_result(cache: DatabaseCache):
    """Decorator for caching function results."""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try to get from cache
            result = cache.get(key)
            if result is not None:
                return result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(key, result)
            return result
        return wrapper
    return decorator

# Global cache instance
query_cache = DatabaseCache()
table_cache = DatabaseCache(max_size=100, ttl=7200)  # Longer TTL for table metadata
