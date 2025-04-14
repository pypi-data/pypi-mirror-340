from igbot_base.exception.base_exception import IgBotBaseException
from igbot_base.tool import Tool


class BaseToolException(IgBotBaseException):

    def __init__(self, message, tool: Tool, cause: Exception = None):
        super().__init__(message, cause)
        self.tool = tool

    def __str__(self):
        result = super().__str__()
        result += f" at tool {self.tool}"

