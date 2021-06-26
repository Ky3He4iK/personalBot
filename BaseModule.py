import abc
from telethon import TelegramClient


class BaseModule(abc.ABC):
    """
        Init module
    """
    def __init__(self, client: TelegramClient):
        self.client = client

    """
        Save state to dictionary
    """
    @staticmethod
    def save_state() -> dict:
        return {}

    """
        Load state from the saved dictionary
    """
    def load_state(self, state: dict, client: TelegramClient):
        self.client = client

    """
        Get list of bot's handlers (telegram.ext.***Handler)
    """
    def get_bot_handlers(self) -> list:
        return []

    """
        Get dict of userbot's handlers (event: async callback func)
    """
    def get_user_handlers(self) -> dict:
        return {}

    """
        Get string that describes this module. Shown to master
    """
    @staticmethod
    @abc.abstractmethod
    def get_module_info() -> str:
        pass


""" To use module create class named `module` that inherits BaseModule like this: """
# module = BaseModule
