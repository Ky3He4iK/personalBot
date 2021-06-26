import logging
from time import sleep
import importlib
from typing import Dict, Tuple
from types import ModuleType

from telegram.ext import Updater, CommandHandler, Filters
from telethon.sync import TelegramClient

import BaseModule
import secret_constants
import config_file

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO,
                    filename="personal.log")
updater = None
client = None
loaded_modules: Dict[str, Tuple[ModuleType, BaseModule.BaseModule]] = {}
states = {}


def init_handers():
    if isinstance(updater, Updater):
        if 1 in updater.dispatcher.handlers:
            for handler in updater.dispatcher.handlers[1]:
                updater.dispatcher.remove_handler(handler, group=1)
        for module, instance in loaded_modules.values():
            for handler in instance.get_bot_handlers():
                updater.dispatcher.add_handler(handler, group=1)
    if isinstance(client, TelegramClient):
        for handler, event in client.list_event_handlers():
            client.remove_event_handler(handler, event)
        for module, instance in loaded_modules.values():
            for event, handler in instance.get_user_handlers().items():
                client.add_event_handler(handler, event)


def reload_handler(update, _):
    logger.warning("Reloading")

    with open('module_list.txt') as module_list:
        new_loaded = module_list.read().splitlines()

    error_text = ""
    for name, (module, instance) in loaded_modules.items():
        states[name] = instance.save_state()
        if name in new_loaded:
            try:
                importlib.reload(module)
                module = __import__(name)
                instance = module.module(client)
                instance.load_state(states[name], client)
                loaded_modules[name] = (module, instance)
            except BaseException as e:
                error_text += f"\nFailed to load module {name}: {e}"
        else:
            del loaded_modules[name]
            del states[name]

    for name in new_loaded:
        if name not in loaded_modules:
            try:
                module = __import__(name)
                instance = module.module(client)
                loaded_modules[name] = (module, instance)
            except BaseException as e:
                error_text += f"\nFailed to load module {name}: {e}"
    init_handers()
    logger.warning("Reloaded")
    if update is not None:
        update.message.reply_text("Reloaded!")


def shutdown_handler(update, _):
    logger.warning("Shutdown")
    update.message.reply_text("Shutdown")
    if isinstance(updater, Updater):
        updater.stop()
    if isinstance(client, TelegramClient):
        client.disconnect()
    sleep(5)
    exit(0)


def modules_handler(update, _):
    text = '\n'.join(f'{name}: {instance.get_module_info()}' for name, (module, instance) in loaded_modules.items())
    update.message.reply_text(text)


# log all errors
def error_handler(update, context):
    logger.error('Error: {} ({} {}) caused.by {}'.format(context, type(context.error), context.error, update))
    print("Error: " + str(context.error))
    if update.message is not None:
        update.message.reply_text("Error")
        context.bot.send_message(chat_id=config_file.master_id, text="Error: {} {} for message {}".format(
            str(type(context.error))[:1000], str(context.error)[:2000], str(update.message.text)[:1000]))


def main():
    global updater
    global client
    updater = Updater(token=secret_constants.bot_token, use_context=True)
    master_commands = {
        'reload': reload_handler,
        'shutdown': shutdown_handler,
        'modules': modules_handler,
    }
    for cmd, handler in master_commands.items():
        updater.dispatcher.add_handler(CommandHandler(
            command=cmd,
            callback=handler,
            filters=Filters.chat(config_file.master_id),
            pass_chat_data=True
        ))
    updater.dispatcher.add_error_handler(error_handler)
    with TelegramClient('personal', secret_constants.api_id, secret_constants.api_hash) as client:
        reload_handler(None, None)

        updater.start_polling()
        client.run_until_disconnected()

        sleep(2)


if __name__ == '__main__':
    main()
