"""
Performance measurement helpers for visualization methods.
"""
import time
from typing import Dict, Any, Callable
import json
from pathlib import Path

def load_metrics_config() -> Dict[str, Any]:
    """Load metrics configuration from JSON file."""
    config_path = Path('config/visualizers/metrics.json')
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {}

def measure_performance(func: Callable) -> Dict[str, Any]:
    """Measure performance metrics for a visualization function."""
    start_time = time.perf_counter()
    start_memory = _get_memory_usage()
    
    result = func()
    
    end_time = time.perf_counter()
    end_memory = _get_memory_usage()
    
    return {
        'execution_time': (end_time - start_time) * 1000,  # ms
        'memory_delta': end_memory - start_memory,  # bytes
        'result': result
    }

def _get_memory_usage() -> int:
    """Get current memory usage."""
    import psutil
    import os
    process = psutil.Process(os.getpid())
    return process.memory_info().rss
