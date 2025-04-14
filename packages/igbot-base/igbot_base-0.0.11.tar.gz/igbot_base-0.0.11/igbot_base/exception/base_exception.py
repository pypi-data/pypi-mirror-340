class IgBotBaseException(Exception):

    def __init__(self, message, cause: Exception = None):
        super().__init__(message)
        self.cause = cause

    def __str__(self):
        result = self.args[0]
        if self.cause:
            result += f" Caused by: {self.cause}"

        return result
