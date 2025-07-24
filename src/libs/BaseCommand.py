from libs import Muzan
from utils import DynamicConfig
from libs import MessageClass


class BaseCommand:
    def __init__(self, client: Muzan, handler, config: dict):
        self.client = client
        self.handler = handler
        self.config = DynamicConfig(config)

    def exec(self, M: MessageClass, arg: DynamicConfig):
        raise NotImplementedError(
            "You must override the exec() method in your Command class."
        )
