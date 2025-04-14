from igbot_base.exception.base_exception import IgBotBaseException
from igbot_base.llmmemory import LlmMemory


class BaseMemoryException(IgBotBaseException):

    def __init__(self, message, memory: LlmMemory, cause: Exception = None):
        super().__init__(message, cause)
        self.memory = memory

    def __str__(self):
        result = super().__str__()
        result += f" at memory {self.memory}"

