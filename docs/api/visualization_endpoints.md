# Visualization API Documentation

## SVG Generation Endpoints

### Particle Simulation
```
POST /api/v1/visualization/particle
```

Request format:
```json
{
    "num_particles": "number",
    "iterations": "number"
}
```

Response format:
```json
{
    "success": true,
    "svg": "string (SVG content)",
    "metrics": {
        "generation_time": "number",
        "memory_usage": "number"
    }
}
```

### Wave Generation
```
POST /api/v1/visualization/wave
```

Request format:
```json
{
    "frequency": "number",
    "amplitude": "number",
    "samples": "number"
}
```

Response format:
```json
{
    "success": true,
    "svg": "string (SVG content)",
    "metrics": {
        "generation_time": "number",
        "memory_usage": "number"
    }
}
```

## Benchmark Endpoints

### Run Performance Benchmarks
```
POST /api/v1/visualization/benchmark
```

Request format:
```json
{
    "iterations": "number"
}
```

Response format:
```json
{
    "success": true,
    "results": {
        "particle": {
            "avg_time": "number",
            "memory_usage": "number"
        },
        "wave": {
            "avg_time": "number",
            "memory_usage": "number"
        }
    },
    "unit": "ms/iteration",
    "iterations": "number"
}
```

## Performance Metrics

| Method | Avg Time (ms) | Memory Usage | Complexity |
|--------|--------------|--------------|------------|
| Particle | 0.8-1.2 | Medium | O(n) |
| Wave | 0.3-0.5 | Low | O(1) |
| Quantum | 0.4-0.6 | Low | O(1) |
| Neural | 1.0-1.5 | High | O(n²) |
| Genetic | 0.7-1.0 | Medium | O(n log n) |
| Chaos | 0.2-0.4 | Low | O(1) |
