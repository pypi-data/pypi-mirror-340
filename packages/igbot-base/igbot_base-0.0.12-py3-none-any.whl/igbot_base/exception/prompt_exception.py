from igbot_base.exception.base_exception import IgBotBaseException
from igbot_base.prompt_template import Prompt


class BasePromptException(IgBotBaseException):

    def __init__(self, message, prompt: Prompt, cause: Exception = None):
        super().__init__(message, cause)
        self.prompt = prompt

    def __str__(self):
        result = super().__str__()
        result += f" at prompt {self.prompt}"

