"""
API Client Utilities

This module provides utilities for interacting with external APIs like OpenAI.
"""
import os
from typing import Optional, Dict, Any
from openai import OpenAI
from ..errors import RuntimeError

class APIClient:
    """
    A wrapper class for API interactions with proper error handling and retry logic.
    """
    
    def __init__(self):
        """Initialize the API client with configuration."""
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def ask_ai(self, prompt: str, model: str = "gpt-3.5-turbo", max_tokens: int = 1000) -> str:
        """
        Send a prompt to the AI model and get a response.
        
        Args:
            prompt: The prompt to send
            model: The model to use
            max_tokens: Maximum tokens in response
            
        Returns:
            The AI's response text
            
        Raises:
            RuntimeError: If the API call fails
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"AI Error: {str(e)}")
