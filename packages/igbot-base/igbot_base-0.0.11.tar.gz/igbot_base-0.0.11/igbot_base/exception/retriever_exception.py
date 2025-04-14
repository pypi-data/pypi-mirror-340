from igbot_base.exception.base_exception import IgBotBaseException
from igbot_base.retriever import Retriever


class BaseRetrieverException(IgBotBaseException):

    def __init__(self, message, retriever: Retriever, cause: Exception = None):
        super().__init__(message, cause)
        self.retriever = retriever

    def __str__(self):
        result = super().__str__()
        result += f" at retriever {self.retriever}"

