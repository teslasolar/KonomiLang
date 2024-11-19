"""
HTML Generator module for Konomi Language
Provides utilities for programmatic HTML generation
"""
from typing import Dict, List, Optional, Union
import html

class HTMLGenerator:
    def __init__(self):
        self.indent_level = 0
        self.indent_size = 2

    def _indent(self) -> str:
        return " " * (self.indent_level * self.indent_size)

    def generate_element(self, tag: str, content: str = "", 
                        attributes: Dict[str, str] = None, 
                        self_closing: bool = False) -> str:
        """Generate an HTML element with the given tag, content, and attributes."""
        attrs = ""
        if attributes:
            attrs = " " + " ".join(f'{k}="{html.escape(str(v))}"' 
                                 for k, v in attributes.items())
        
        if self_closing:
            return f"{self._indent()}<{tag}{attrs}/>\n"
        
        return f"{self._indent()}<{tag}{attrs}>{content}</{tag}>\n"

    def generate_container(self, tag: str, children: List[str], 
                         attributes: Dict[str, str] = None) -> str:
        """Generate a container element with nested children."""
        attrs = ""
        if attributes:
            attrs = " " + " ".join(f'{k}="{html.escape(str(v))}"' 
                                 for k, v in attributes.items())
        
        result = f"{self._indent()}<{tag}{attrs}>\n"
        self.indent_level += 1
        for child in children:
            result += child
        self.indent_level -= 1
        result += f"{self._indent()}</{tag}>\n"
        return result

    def generate_document(self, title: str, content: str, 
                         styles: Optional[str] = None) -> str:
        """Generate a complete HTML document."""
        doc = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{html.escape(title)}</title>
    {'<style>' + styles + '</style>' if styles else ''}
</head>
<body>
{content}</body>
</html>
"""
        return doc
