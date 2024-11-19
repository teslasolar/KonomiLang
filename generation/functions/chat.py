class ChatGenerator:
    def __init__(self):
        self.max_messages = 50
        self.default_params = {
            "temperature": 0.8,
            "max_tokens": 150,
            "presence_penalty": 0.0,
            "frequency_penalty": 0.0
        }
        self.allowed_roles = ["system", "user", "assistant"]

    def validate_messages(self, messages):
        if not messages or not isinstance(messages, list):
            raise ValueError("Messages must be a non-empty list")
        
        if len(messages) > self.max_messages:
            raise ValueError(f"Number of messages exceeds maximum of {self.max_messages}")
        
        for message in messages:
            if not isinstance(message, dict):
                raise ValueError("Each message must be a dictionary")
            
            if "role" not in message or "content" not in message:
                raise ValueError("Messages must contain 'role' and 'content' keys")
            
            if message["role"] not in self.allowed_roles:
                raise ValueError(f"Invalid role. Must be one of: {', '.join(self.allowed_roles)}")
        
        return True

    def validate_params(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be a dictionary")
        
        if "temperature" in params and not 0 <= params["temperature"] <= 2:
            raise ValueError("Temperature must be between 0 and 2")
        
        if "max_tokens" in params and params["max_tokens"] < 1:
            raise ValueError("max_tokens must be positive")
        
        return True

    def generate(self, messages, params=None):
        try:
            self.validate_messages(messages)
            
            generation_params = self.default_params.copy()
            if params:
                self.validate_params(params)
                generation_params.update(params)
            
            # Call OpenAI API here
            # This is a placeholder for the actual API call
            response = {
                "message": {
                    "role": "assistant",
                    "content": "Generated response would appear here"
                },
                "usage": {
                    "prompt_tokens": 50,
                    "completion_tokens": 30,
                    "total_tokens": 80
                },
                "model": "gpt-3.5-turbo"
            }
            
            return response
            
        except Exception as e:
            raise Exception(f"Chat generation failed: {str(e)}")
