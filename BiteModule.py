import re

from telegram.ext import MessageHandler, Filters

from BaseModule import *
import config_file


class BiteModule(BaseModule):
    def __init__(self, client: TelegramClient):
        super().__init__(client)

    def get_bot_handlers(self) -> list:
        return [
            MessageHandler(Filters.regex(re.compile('Кусь.*', re.IGNORECASE)), self.bite_handler)
        ]

    @staticmethod
    def bite_handler(update, context):
        if update.message.chat_id == config_file.master_id or update.message.from_user.id == config_file.master_id:
            context.bot.send_message(config_file.cutie_id, update.message.text)
        elif update.message.chat_id == config_file.cutie_id or update.message.from_user.id == config_file.cutie_id:
            context.bot.send_message(config_file.master_id, update.message.text)
        context.bot.send_message(config_file.master_id, str(update.message.chat_id))


module = BiteModule
