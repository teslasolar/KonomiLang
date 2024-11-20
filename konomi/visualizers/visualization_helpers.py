"""
SVG generation and rendering helpers for visualization methods.
"""
from typing import List, Dict, Any, Union

def generate_particle_svg(data: List[Dict[str, float]]) -> str:
    """Generate SVG for particle simulation."""
    particles = ' '.join([
        f'<circle cx="{p["x"]}" cy="{p["y"]}" r="2" fill="#93e"/>'
        for p in data
    ])
    return f'<svg viewBox="0 0 100 100">{particles}</svg>'

def generate_wave_svg(data: List[float]) -> str:
    """Generate SVG for wave pattern."""
    points = ' '.join([f'{i*2},{y}' for i, y in enumerate(data)])
    return f'''
    <svg viewBox="0 0 100 100">
        <path d="M {points}" stroke="#93e" fill="none"/>
    </svg>
    '''

def generate_quantum_svg(data: List[int]) -> str:
    """Generate SVG for quantum states."""
    states = ' '.join([
        f'<circle cx="{i*2}" cy="{val}" r="2" fill="#93e"/>'
        for i, val in enumerate(data)
    ])
    return f'<svg viewBox="0 0 100 100">{states}</svg>'

def generate_neural_svg(data: List[List[int]]) -> str:
    """Generate SVG for neural network."""
    nodes = []
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            if val:
                nodes.append(f'<circle cx="{i*10+10}" cy="{j*10+10}" r="4" fill="#93e"/>')
    return f'<svg viewBox="0 0 100 100">{"".join(nodes)}</svg>'

def generate_genetic_svg(data: List[float]) -> str:
    """Generate SVG for genetic algorithm."""
    points = ' '.join([f'{i*2},{val*100}' for i, val in enumerate(data)])
    return f'''
    <svg viewBox="0 0 100 100">
        <path d="M {points}" stroke="#93e" fill="none"/>
    </svg>
    '''

def generate_chaos_svg(data: List[float]) -> str:
    """Generate SVG for chaos system."""
    points = ' '.join([f'{i*2},{val*100}' for i, val in enumerate(data)])
    return f'''
    <svg viewBox="0 0 100 100">
        <path d="M {points}" stroke="#93e" fill="none"/>
    </svg>
    '''
