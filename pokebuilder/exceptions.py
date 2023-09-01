class ConfigNotFoundException(Exception):
    def __init__(self, message="Configuration file not found"):
        super().__init__(message)


class DatabasePopulationException(Exception):
    def __init__(self, message="Results were expected from database query"):
        super().__init__(message)
