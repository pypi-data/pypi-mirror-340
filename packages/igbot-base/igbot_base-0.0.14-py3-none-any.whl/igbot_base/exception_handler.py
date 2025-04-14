from abc import ABC, abstractmethod

from igbot_base.agent_response import AgentResponse

from igbot_base.igbot_base.exception.llm_exception import BaseLlmException


class ExceptionHandler(ABC):

    @abstractmethod
    def handle(self, e: Exception):
        pass


class NoopExceptionHandler(ExceptionHandler):

    def handle(self, e: Exception):
        pass


class PrintingExceptionHandler(ExceptionHandler):

    def handle(self, e: Exception):
        print(e)


class ReturnFailedResponseGracefully(ExceptionHandler):

    def handle(self, e: Exception):
        return AgentResponse.error(str(e), e)

