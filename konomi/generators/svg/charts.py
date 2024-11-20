"""
SVG Chart Generation functionality
Provides utilities for generating various types of charts (bar, line, pie)
"""
from typing import Dict, List, Optional, Tuple, Union
from .core import SVGGenerator
from .validation import SVGValidator
import math

class ChartGenerator(SVGGenerator):
    """Generates SVG charts with customizable styling and animations."""
    
    def __init__(self, width: int = 600, height: int = 400, 
                 margin: Optional[Dict[str, int]] = None):
        super().__init__(width, height)
        self.margin = margin or {"top": 40, "right": 40, "bottom": 50, "left": 60}
        self.validator = SVGValidator()
        
    def _calculate_scales(self, data: List[float], height: int) -> Tuple[float, float]:
        """Calculate scale factors for data visualization."""
        if not data:
            return 0, 0
        data_max = max(data)
        data_min = min(min(data), 0)  # Ensure negative values are handled
        data_range = data_max - data_min
        if data_range == 0:
            return 0, data_min
        scale = height / data_range
        return scale, data_min

    def generate_bar_chart(self, data: List[float], labels: List[str], 
                          title: str = "", colors: Optional[List[str]] = None) -> str:
        """Generate a bar chart.
        
        Args:
            data: List of numerical values
            labels: List of labels for each bar
            title: Chart title
            colors: Optional list of colors for bars
        """
        if len(data) != len(labels):
            raise ValueError("Data and labels must have the same length")
            
        # Calculate dimensions
        chart_width = self.width - self.margin["left"] - self.margin["right"]
        chart_height = self.height - self.margin["top"] - self.margin["bottom"]
        
        # Calculate scales
        scale, min_value = self._calculate_scales(data, chart_height)
        bar_width = chart_width / len(data) * 0.8
        spacing = chart_width / len(data) * 0.2
        
        # Generate bars
        bars = []
        for i, (value, label) in enumerate(zip(data, labels)):
            x = self.margin["left"] + (i * (bar_width + spacing))
            height = abs(value - min_value) * scale
            y = self.margin["top"] + (chart_height - height if value >= 0 else chart_height)
            
            color = colors[i] if colors and i < len(colors) else f"hsl({(i * 360/len(data))}, 70%, 50%)"
            
            # Add bar with animation
            bar_id = f"bar-{i}"
            bars.append(
                f'<rect id="{bar_id}" x="{x}" y="{y}" width="{bar_width}" '
                f'height="{height}" fill="{color}" opacity="0.8">'
                f'<title>{label}: {value}</title>'
                f'</rect>'
            )
            
            # Add label
            bars.append(
                f'<text x="{x + bar_width/2}" y="{self.height - self.margin["bottom"] + 20}" '
                f'text-anchor="middle" font-size="12">{label}</text>'
            )
        
        # Add title
        if title:
            bars.append(
                f'<text x="{self.width/2}" y="{self.margin["top"]/2}" '
                f'text-anchor="middle" font-size="16" font-weight="bold">{title}</text>'
            )
        
        # Add y-axis
        y_axis = self._generate_y_axis(min_value, max(data), chart_height)
        
        # Combine elements
        self.elements.extend(bars)
        self.elements.extend(y_axis)
        
        return self.generate()
        
    def generate_line_chart(self, data: List[float], labels: List[str],
                           title: str = "", line_color: str = "#4C6EF5") -> str:
        """Generate a line chart.
        
        Args:
            data: List of numerical values
            labels: List of labels for each point
            title: Chart title
            line_color: Color of the line
        """
        if len(data) != len(labels):
            raise ValueError("Data and labels must have the same length")
            
        # Calculate dimensions
        chart_width = self.width - self.margin["left"] - self.margin["right"]
        chart_height = self.height - self.margin["top"] - self.margin["bottom"]
        
        # Calculate scales
        scale, min_value = self._calculate_scales(data, chart_height)
        point_spacing = chart_width / (len(data) - 1) if len(data) > 1 else 0
        
        # Generate path data
        path_data = []
        points = []
        
        for i, (value, label) in enumerate(zip(data, labels)):
            x = self.margin["left"] + (i * point_spacing)
            y = self.margin["top"] + (chart_height - (value - min_value) * scale)
            
            if i == 0:
                path_data.append(f"M {x} {y}")
            else:
                path_data.append(f"L {x} {y}")
            
            # Add point and hover effect
            point_id = f"point-{i}"
            points.append(
                f'<circle id="{point_id}" cx="{x}" cy="{y}" r="4" '
                f'fill="{line_color}" stroke="white" stroke-width="2">'
                f'<title>{label}: {value}</title>'
                f'</circle>'
            )
            
            # Add label
            points.append(
                f'<text x="{x}" y="{self.height - self.margin["bottom"] + 20}" '
                f'text-anchor="middle" font-size="12">{label}</text>'
            )
        
        # Add path
        path = f'<path d="{" ".join(path_data)}" fill="none" stroke="{line_color}" stroke-width="2"/>'
        
        # Add title
        if title:
            points.append(
                f'<text x="{self.width/2}" y="{self.margin["top"]/2}" '
                f'text-anchor="middle" font-size="16" font-weight="bold">{title}</text>'
            )
        
        # Add y-axis
        y_axis = self._generate_y_axis(min_value, max(data), chart_height)
        
        # Combine elements
        self.elements.append(path)
        self.elements.extend(points)
        self.elements.extend(y_axis)
        
        return self.generate()

    def generate_pie_chart(self, data: List[float], labels: List[str],
                          title: str = "", colors: Optional[List[str]] = None) -> str:
        """Generate a pie chart.
        
        Args:
            data: List of numerical values
            labels: List of labels for each slice
            title: Chart title
            colors: Optional list of colors for slices
        """
        if len(data) != len(labels):
            raise ValueError("Data and labels must have the same length")
            
        total = sum(data)
        if total == 0:
            raise ValueError("Data sum cannot be zero")
            
        # Calculate center and radius
        center_x = self.width / 2
        center_y = self.height / 2
        radius = min(center_x - self.margin["left"], 
                    center_y - self.margin["top"]) * 0.8
        
        # Generate slices
        slices = []
        current_angle = 0
        
        for i, (value, label) in enumerate(zip(data, labels)):
            percentage = value / total
            angle = percentage * 2 * math.pi
            end_angle = current_angle + angle
            
            # Calculate path coordinates
            start_x = center_x + radius * math.cos(current_angle)
            start_y = center_y + radius * math.sin(current_angle)
            end_x = center_x + radius * math.cos(end_angle)
            end_y = center_y + radius * math.sin(end_angle)
            
            # Large arc flag is 1 if angle > π
            large_arc = 1 if angle > math.pi else 0
            
            color = colors[i] if colors and i < len(colors) else f"hsl({(i * 360/len(data))}, 70%, 50%)"
            
            # Create slice path
            slice_id = f"slice-{i}"
            path_data = (
                f"M {center_x} {center_y} "
                f"L {start_x} {start_y} "
                f"A {radius} {radius} 0 {large_arc} 1 {end_x} {end_y} Z"
            )
            
            slices.append(
                f'<path id="{slice_id}" d="{path_data}" fill="{color}" '
                f'opacity="0.8" cursor="pointer">'
                f'<title>{label}: {value} ({percentage:.1%})</title>'
                f'</path>'
            )
            
            # Add label
            label_angle = current_angle + angle/2
            label_x = center_x + (radius + 30) * math.cos(label_angle)
            label_y = center_y + (radius + 30) * math.sin(label_angle)
            
            slices.append(
                f'<text x="{label_x}" y="{label_y}" '
                f'text-anchor="{("end" if label_x < center_x else "start")}" '
                f'alignment-baseline="middle" font-size="12">'
                f'{label} ({percentage:.1%})</text>'
            )
            
            current_angle = end_angle
        
        # Add title
        if title:
            slices.append(
                f'<text x="{self.width/2}" y="{self.margin["top"]/2}" '
                f'text-anchor="middle" font-size="16" font-weight="bold">{title}</text>'
            )
        
        # Combine elements
        self.elements.extend(slices)
        
        return self.generate()

    def _generate_y_axis(self, min_value: float, max_value: float, 
                        height: int, ticks: int = 5) -> List[str]:
        """Generate y-axis elements."""
        elements = []
        
        # Add axis line
        elements.append(
            f'<line x1="{self.margin["left"]}" y1="{self.margin["top"]}" '
            f'x2="{self.margin["left"]}" y2="{self.height - self.margin["bottom"]}" '
            f'stroke="black" stroke-width="1"/>'
        )
        
        # Add ticks and labels
        value_range = max_value - min_value
        tick_step = value_range / (ticks - 1) if ticks > 1 else value_range
        
        for i in range(ticks):
            y_pos = self.height - self.margin["bottom"] - (i * height / (ticks - 1))
            value = min_value + (i * tick_step)
            
            # Add tick
            elements.append(
                f'<line x1="{self.margin["left"] - 5}" y1="{y_pos}" '
                f'x2="{self.margin["left"]}" y2="{y_pos}" '
                f'stroke="black" stroke-width="1"/>'
            )
            
            # Add label
            elements.append(
                f'<text x="{self.margin["left"] - 10}" y="{y_pos}" '
                f'text-anchor="end" alignment-baseline="middle" font-size="12">'
                f'{value:.1f}</text>'
            )
        
        return elements
