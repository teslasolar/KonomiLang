class CodeGenerator:
    def __init__(self):
        self.supported_languages = ["python", "javascript", "java", "cpp", "rust"]
        self.default_params = {
            "temperature": 0.3,
            "max_tokens": 500,
            "stop": ["```"]
        }

    def validate_prompt(self, prompt, language=None):
        if not prompt or not isinstance(prompt, str):
            raise ValueError("Prompt must be a non-empty string")
        
        if language and language not in self.supported_languages:
            raise ValueError(f"Unsupported language. Must be one of: {', '.join(self.supported_languages)}")
        
        return True

    def validate_params(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be a dictionary")
        
        if "temperature" in params and not 0 <= params["temperature"] <= 2:
            raise ValueError("Temperature must be between 0 and 2")
        
        if "max_tokens" in params and params["max_tokens"] < 1:
            raise ValueError("max_tokens must be positive")
        
        return True

    def validate_code(self, code):
        # Basic syntax validation
        # In a real implementation, this would use language-specific parsers
        if not code or not isinstance(code, str):
            raise ValueError("Invalid code output")
        return True

    def generate(self, prompt, language="python", params=None):
        try:
            self.validate_prompt(prompt, language)
            
            generation_params = self.default_params.copy()
            if params:
                self.validate_params(params)
                generation_params.update(params)
            
            # Call OpenAI API here
            # This is a placeholder for the actual API call
            response = {
                "code": "def hello_world():\n    print('Hello, World!')",
                "language": language,
                "usage": {
                    "prompt_tokens": len(prompt.split()),
                    "completion_tokens": 20,
                    "total_tokens": len(prompt.split()) + 20
                }
            }
            
            self.validate_code(response["code"])
            return response
            
        except Exception as e:
            raise Exception(f"Code generation failed: {str(e)}")
