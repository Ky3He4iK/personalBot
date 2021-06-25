from telethon import TelegramClient


class BaseModule:
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


""" To use module create class named `module` that inherits BaseModule like this: """
# module = BaseModule
