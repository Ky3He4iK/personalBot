from telegram.ext import CommandHandler

from BaseModule import *
import config_file


class StartModule(BaseModule):
    def __init__(self, client: TelegramClient):
        super().__init__(client)

    def get_bot_handlers(self) -> list:
        return [
            CommandHandler('start', self.start_handler),
        ]

    @staticmethod
    def start_handler(update, _):
        if update.message.chat_id == config_file.master_id or update.message.from_user.id == config_file.master_id:
            update.message.reply_text("Senpai!\n/reload\n/shutdown")
        elif update.message.chat_id == config_file.cutie_id or update.message.from_user.id == config_file.cutie_id:
            update.message.reply_text("Мяу 😻")
        else:
            update.message.reply_text("Тебе здесь не рады, кожаный мешок!!")


module = StartModule
