class CompletionGenerator:
    def __init__(self):
        self.max_prompt_length = 4000
        self.default_params = {
            "temperature": 0.7,
            "max_tokens": 150,
            "top_p": 1.0
        }

    def validate_prompt(self, prompt):
        if not prompt or not isinstance(prompt, str):
            raise ValueError("Prompt must be a non-empty string")
        
        if len(prompt) > self.max_prompt_length:
            raise ValueError(f"Prompt length exceeds maximum of {self.max_prompt_length} characters")
        
        return True

    def validate_params(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be a dictionary")
        
        if "temperature" in params and not 0 <= params["temperature"] <= 2:
            raise ValueError("Temperature must be between 0 and 2")
        
        if "max_tokens" in params and params["max_tokens"] < 1:
            raise ValueError("max_tokens must be positive")
        
        if "top_p" in params and not 0 <= params["top_p"] <= 1:
            raise ValueError("top_p must be between 0 and 1")
        
        return True

    def generate(self, prompt, params=None):
        try:
            self.validate_prompt(prompt)
            
            generation_params = self.default_params.copy()
            if params:
                self.validate_params(params)
                generation_params.update(params)
            
            # Call OpenAI API here
            # This is a placeholder for the actual API call
            response = {
                "text": "Generated text would appear here",
                "usage": {
                    "prompt_tokens": len(prompt.split()),
                    "completion_tokens": 50,
                    "total_tokens": len(prompt.split()) + 50
                },
                "model": "text-davinci-003"
            }
            
            return response
            
        except Exception as e:
            raise Exception(f"Generation failed: {str(e)}")
