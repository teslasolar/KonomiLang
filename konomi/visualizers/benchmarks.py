"""
Visualization benchmarks module providing a common interface for benchmarking different visualization methods.
"""
from typing import Dict, Any, List
import json
from pathlib import Path

from .data_generators import (
    generate_particle_data, generate_wave_data, generate_quantum_data,
    generate_neural_network_data, generate_genetic_data, generate_chaos_data
)
from .benchmark_helpers import run_benchmark_suite
from .visualization_helpers import (
    generate_particle_svg, generate_wave_svg, generate_quantum_svg,
    generate_neural_svg, generate_genetic_svg, generate_chaos_svg
)
from .metrics_helpers import measure_performance, load_metrics_config

class VisualizationBenchmark:
    """Base class for visualization benchmarks."""
    def __init__(self):
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load benchmark configuration."""
        config_path = Path('config/visualizers/benchmarks.json')
        if config_path.exists():
            with open(config_path) as f:
                return json.load(f)
        return {}
        
    def run(self, iterations: int = None) -> Dict[str, Any]:
        """Run the benchmark for given iterations."""
        if iterations is None:
            iterations = self.config.get('default_iterations', 100)
            
        return run_benchmark_suite(self._execute_iteration, iterations)

    def _execute_iteration(self):
        """Execute a single iteration of the benchmark."""
        raise NotImplementedError()

class ParticleSimulationBenchmark(VisualizationBenchmark):
    def _execute_iteration(self):
        data = generate_particle_data()
        return generate_particle_svg(data)

class WaveGenerationBenchmark(VisualizationBenchmark):
    def __init__(self):
        super().__init__()
        self.t = 0

    def _execute_iteration(self):
        self.t += 0.1
        data = generate_wave_data(self.t)
        return generate_wave_svg(data)

class QuantumVisualizationBenchmark(VisualizationBenchmark):
    def _execute_iteration(self):
        data = generate_quantum_data()
        return generate_quantum_svg(data)

class NeuralNetworkBenchmark(VisualizationBenchmark):
    def _execute_iteration(self):
        data = generate_neural_network_data()
        return generate_neural_svg(data)

class GeneticAlgorithmBenchmark(VisualizationBenchmark):
    def _execute_iteration(self):
        data = generate_genetic_data()
        return generate_genetic_svg(data)

class ChaosBenchmark(VisualizationBenchmark):
    def _execute_iteration(self):
        data = [generate_chaos_data() for _ in range(50)]
        return generate_chaos_svg(data)

def run_all_benchmarks(iterations: int = None) -> Dict[str, Any]:
    """Run all visualization benchmarks and return results."""
    benchmarks = {
        'particle': ParticleSimulationBenchmark(),
        'wave': WaveGenerationBenchmark(),
        'quantum': QuantumVisualizationBenchmark(),
        'neural': NeuralNetworkBenchmark(),
        'genetic': GeneticAlgorithmBenchmark(),
        'chaos': ChaosBenchmark()
    }
    
    metrics_config = load_metrics_config()
    results = {}
    
    for name, benchmark in benchmarks.items():
        benchmark_result = benchmark.run(iterations)
        results[name] = {
            'benchmark': benchmark_result,
            'metrics': metrics_config.get(name, {})
        }
    
    return results
