from igbot_base.exception.base_exception import IgBotBaseException
from igbot_base.llm import Llm


class BaseLlmException(IgBotBaseException):

    def __init__(self, message, llm: Llm,  cause: Exception = None):
        super().__init__(message, cause)
        self.llm = llm

    def __str__(self):
        result = super().__str__()
        result += f" at llm {self.llm}"
