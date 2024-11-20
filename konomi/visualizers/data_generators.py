"""
Data generation module for different visualization methods.
"""
import random
import math
from typing import List, Dict, Any

def generate_particle_data(num_particles: int = 99) -> List[Dict[str, float]]:
    """Generate particle simulation data."""
    return [{
        'x': random.random() * 99,
        'y': random.random() * 99,
        'v': random.random() - 0.5,
        'w': random.random() - 0.5
    } for _ in range(num_particles)]

def generate_wave_data(time_step: float = 0.1) -> List[float]:
    """Generate wave pattern data."""
    return [50 + 25 * math.sin(time_step) + 15 * math.cos(time_step * 1.5) for _ in range(50)]

def generate_quantum_data() -> List[int]:
    """Generate quantum state data."""
    return [99 if random.random() > 0.5 else 0 for _ in range(50)]

def generate_neural_network_data() -> List[List[int]]:
    """Generate neural network activity data."""
    return [[1 if random.random() > 0.7 else 0 for _ in range(9)] for _ in range(9)]

def generate_genetic_data(population_size: int = 50) -> List[float]:
    """Generate genetic algorithm population data."""
    return sorted([random.random() for _ in range(population_size)])

def generate_chaos_data(x: float = 0.5) -> float:
    """Generate chaos system data point."""
    return 4 * x * (1 - x)
