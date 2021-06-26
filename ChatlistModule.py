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
        return "/chats - list all chats\n/chats N - list first N chats"

    async def get_dialogs(self, limit=None):
        res = ""
        async for dialog in self.client.iter_dialogs(limit=limit):
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
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        done, pending = loop.run_until_complete(asyncio.wait([task]))
        return list(done)[0].result()

    def chats_handler(self, update, _):
        if ' ' in update.message.text:
            limit = int(update.message.text.split(' ')[1])
        else:
            limit = None
        text = self.run_async(self.get_dialogs(limit))
        while len(text) > 4095:
            last = text[:4096].rfind('\n')
            if last == -1:
                update.message.reply_text(text[:4092] + '...', parse_mode=ParseMode.MARKDOWN_V2)
                text = text[4092:]
            else:
                update.message.reply_text(text[:last])
                text = text[last + 1:]
            update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN_V2)


module = ChatlistModule
