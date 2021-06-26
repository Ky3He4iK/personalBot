import asyncio
from telegram.ext import CommandHandler
from telegram import ParseMode

from BaseModule import *
import config_file


class ChatlistModule(BaseModule):
    def __init__(self, client: TelegramClient):
        super().__init__(client)

    def get_bot_handlers(self) -> list:
        return [
            CommandHandler('chats', self.chats_handler)
        ]

    @staticmethod
    def get_module_info() -> str:
        return "/chats - list all chats"

    async def get_dialogs(self):
        res = ""
        for dialog in self.client.iter_dialogs():
            res += f"\n`{dialog.id}`: {self.escape_markdown_v2(str(dialog.title))}"
        return res

    @staticmethod
    def escape_markdown_v2(text):
        blacklisted = '*-_~`[]()'
        for char in blacklisted:
            text = text.replace(char, '\\' + char)
        return text

    @staticmethod
    def run_async(task):
        loop = asyncio.get_event_loop()
        done, pending = loop.run_until_complete(asyncio.wait([task]))
        return list(done)[0].result()

    def chats_handler(self, update, _):
        dialogs = self.run_async(self.get_dialogs)
        update.message.reply_text(dialogs, parse_mode=ParseMode.MARKDOWN_V2)


module = ChatlistModule
