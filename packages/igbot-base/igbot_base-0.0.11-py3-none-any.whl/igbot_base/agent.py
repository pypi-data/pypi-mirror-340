from abc import ABC, abstractmethod

from igbot_base.agent_response import AgentResponse


class Agent(ABC):

    @abstractmethod
    def invoke(self, query) -> AgentResponse:
        pass

    @abstractmethod
    def describe(self):
        pass

    def __str__(self):
        return self.describe()