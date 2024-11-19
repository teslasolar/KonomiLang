"""
Markdown Processing Utilities

This module provides utilities for processing markdown content
and code highlighting.
"""
import markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

def process_markdown(content, extensions=None):
    """
    Process markdown content with specified extensions.
    
    Args:
        content: Markdown content to process
        extensions: List of markdown extensions to use
        
    Returns:
        Processed HTML content
    """
    if extensions is None:
        extensions = ['fenced_code', 'codehilite', 'tables', 'attr_list']
    return markdown.markdown(content, extensions=extensions)

def highlight_code(code, language='konomi'):
    """
    Syntax highlight code snippets.
    
    Args:
        code: Code to highlight
        language: Programming language for syntax highlighting
        
    Returns:
        HTML-formatted highlighted code
    """
    try:
        lexer = get_lexer_by_name(language)
        formatter = HtmlFormatter(style='monokai', cssclass='highlight')
        return highlight(code, lexer, formatter)
    except:
        return code
