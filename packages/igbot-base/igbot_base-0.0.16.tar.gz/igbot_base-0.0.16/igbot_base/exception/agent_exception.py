from igbot_base.agent import Agent
from igbot_base.exception.base_exception import IgBotBaseException


class BaseAgentException(IgBotBaseException):

    def __init__(self, message, agent: Agent, cause: Exception = None):
        super().__init__(message, cause)
        self.agent = agent

    def __str__(self):
        result = super().__str__()
        result += f" at agent {self.agent}"

