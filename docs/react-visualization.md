# React-Based Compression and Visualization Methods

## Overview
This documentation covers the various visualization and compression techniques implemented in our React components. These methods provide interactive visualizations for different types of data and algorithms.

## Visualization Methods

### 1. Particle Simulation (sim.p)
```typescript
sim.p(): IntervalID
```
A particle system simulation that creates an interactive field of particles.

#### Implementation Details:
- Creates 99 particles with random initial positions and velocities
- Updates particle positions using velocity vectors
- Handles boundary collisions with elastic reflection
- Aggregates particle positions for visualization
- Updates every 50ms

#### Usage Example:
```jsx
const ParticleVis = () => {
  useEffect(() => {
    const interval = sim.p();
    return () => clearInterval(interval);
  }, []);
  return <G d={particleData} i="particles" />;
};
```

### 2. Wave Generation (sim.w)
```typescript
sim.w(): IntervalID
```
Generates and visualizes complex wave patterns using trigonometric functions.

#### Implementation Details:
- Combines sine and cosine waves with different frequencies
- Updates wave pattern every 50ms
- Creates smooth, animated wave motion
- Parameters: Base amplitude of 25, variable frequency

#### Usage Example:
```jsx
const WaveVis = () => {
  useEffect(() => {
    const interval = sim.w();
    return () => clearInterval(interval);
  }, []);
  return <G d={waveData} i="wave" />;
};
```

### 3. Quantum State Visualization (sim.q)
```typescript
sim.q(): IntervalID
```
Visualizes quantum state transitions using binary state representation.

#### Implementation Details:
- Generates binary quantum states (0 or 99)
- Updates every 99ms
- Useful for quantum computing state visualization
- Creates a clear visual distinction between states

#### Usage Example:
```jsx
const QuantumVis = () => {
  useEffect(() => {
    const interval = sim.q();
    return () => clearInterval(interval);
  }, []);
  return <G d={quantumData} i="quantum" />;
};
```

### 4. Neural Network Activity (sim.n)
```typescript
sim.n(): IntervalID
```
Visualizes neural network activity patterns in a 9x9 grid.

#### Implementation Details:
- Simulates neuron activation patterns
- Updates every 200ms
- Represents active neurons with value 1
- Aggregates activation density for visualization

#### Usage Example:
```jsx
const NeuralVis = () => {
  useEffect(() => {
    const interval = sim.n();
    return () => clearInterval(interval);
  }, []);
  return <G d={neuralData} i="neural" />;
};
```

### 5. Genetic Algorithm Visualization (sim.g)
```typescript
sim.g(): IntervalID
```
Visualizes genetic algorithm population distribution.

#### Implementation Details:
- Maintains a population of 50 entities
- Applies random mutations every 99ms
- Sorts population to show distribution
- Useful for evolutionary algorithm visualization

#### Usage Example:
```jsx
const GeneticVis = () => {
  useEffect(() => {
    const interval = sim.g();
    return () => clearInterval(interval);
  }, []);
  return <G d={geneticData} i="genetic" />;
};
```

### 6. Chaos System Visualization (sim.c)
```typescript
sim.c(): IntervalID
```
Visualizes chaotic system behavior using the logistic map.

#### Implementation Details:
- Implements the logistic map equation (x = 4x(1-x))
- Updates every 50ms
- Shows chaotic pattern emergence
- Useful for demonstrating chaos theory concepts

#### Usage Example:
```jsx
const ChaosVis = () => {
  useEffect(() => {
    const interval = sim.c();
    return () => clearInterval(interval);
  }, []);
  return <G d={chaosData} i="chaos" />;
};
```

## SVG Visualization Component (G)
```typescript
interface GProps {
  d: number[];  // Data array for visualization
  i: string;    // Unique identifier for gradient
}
```
A reusable SVG visualization component that renders data with gradient effects.

### Implementation Details:
- Viewport: 100x50 units
- Gradient: Purple (#93e) with variable opacity
- Path rendering with area fill
- Automatic scaling of input data

### Usage Example:
```jsx
<G d={[50, 60, 70, 65, 55]} i="example" />
```

## Common Patterns and Best Practices

1. **Cleanup Pattern**
```jsx
useEffect(() => {
  const interval = sim.method();
  return () => clearInterval(interval);
}, []);
```

2. **Data Management**
- Keep data arrays at fixed length (50 points)
- Use slice(1) for FIFO updates
- Normalize values to 0-99 range

3. **Performance Considerations**
- All intervals run at 50-200ms
- Use appropriate cleanup to prevent memory leaks
- Implement shouldComponentUpdate for optimization

## Error Handling
```jsx
try {
  const interval = sim.method();
  // Handle visualization
} catch (error) {
  console.error('Visualization error:', error);
  // Implement fallback visualization
}
```
