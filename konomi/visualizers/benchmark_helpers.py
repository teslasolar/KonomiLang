"""
Benchmark utility functions for visualization methods.
"""
import time
from typing import Callable, Any, Dict

def measure_execution_time(func: Callable, *args, **kwargs) -> float:
    """Measure execution time of a function in milliseconds."""
    start = time.perf_counter()
    func(*args, **kwargs)
    return (time.perf_counter() - start) * 1000

def collect_memory_usage(func: Callable, *args, **kwargs) -> Dict[str, Any]:
    """Collect memory usage statistics for a function."""
    import tracemalloc
    
    tracemalloc.start()
    func(*args, **kwargs)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    return {
        'current': current / 1024,  # KB
        'peak': peak / 1024  # KB
    }

def run_benchmark_suite(func: Callable, iterations: int = 100) -> Dict[str, Any]:
    """Run complete benchmark suite for a visualization function."""
    execution_times = []
    memory_stats = None
    
    # Time measurements
    for _ in range(iterations):
        execution_times.append(measure_execution_time(func))
    
    # Memory measurement (once)
    memory_stats = collect_memory_usage(func)
    
    return {
        'avg_time': sum(execution_times) / len(execution_times),
        'min_time': min(execution_times),
        'max_time': max(execution_times),
        'memory_usage': memory_stats
    }
