class ConfigNotFoundException(Exception):
    def __init__(self, message="Configuration file not found"):
        super().__init__(message)