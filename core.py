from telegram.ext import Updater, CommandHandler, Filters
from telethon.sync import TelegramClient, events
import logging


import main_functions
import secret_constants
from time import sleep
import importlib

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO, filename="rollbot.log")
updater = None
client = None


def init_handers():
    if isinstance(updater, Updater):
        if 1 in updater.dispatcher.handlers:
            for handler in updater.dispatcher.handlers[1]:
                updater.dispatcher.remove_handler(handler, group=1)
        for handler in main_functions.get_handlers():
            updater.dispatcher.add_handler(handler, group=1)
    if isinstance(client, TelegramClient):
        for handler, event in client.list_event_handlers():
            client.remove_event_handler(handler, event)
        for event, handler in main_functions.get_user_handlers().items():
            client.add_event_handler(handler, event)


def reload_handler(update, _):
    global main_functions
    logger.warning("Reloading")
    state = main_functions.save_state()

    importlib.reload(main_functions)
    import main_functions

    main_functions.load_state(state, client)
    init_handers()
    logger.warning("Reloaded")
    update.message.reply_text("Reloaded!")


def shutdown_handler(update, _):
    logger.warning("Shutdown")
    update.message.reply_text("Shutdown")
    if isinstance(updater, Updater):
        updater.stop()
    if isinstance(client, TelegramClient):
        client.disconnect()
    sleep(10)
    exit(0)


# log all errors
def error_handler(update, context):
    logger.error('Error: {} ({} {}) caused.by {}'.format(context, type(context.error), context.error, update))
    print("Error: " + str(context.error))
    if update.message is not None:
        update.message.reply_text("Error")
        context.bot.send_message(chat_id=secret_constants.master_id, text="Error: {} {} for message {}".format(
            str(type(context.error))[:1000], str(context.error)[:2000], str(update.message.text)[:1000]))


def main():
    global updater
    global client
    updater = Updater(token=secret_constants.bot_token, use_context=True)
    master_commands = {
        'reload': reload_handler,
        'shutdown': shutdown_handler,
    }
    for cmd, handler in master_commands.items():
        updater.dispatcher.add_handler(CommandHandler(
            command=cmd,
            callback=handler,
            filters=Filters.chat(secret_constants.master_id),
            pass_chat_data=True
        ))
    updater.dispatcher.add_error_handler(error_handler)
    with TelegramClient('personal', secret_constants.api_id, secret_constants.api_hash) as client:
        init_handers()
        main_functions.init_state()

        updater.start_polling()
        client.run_until_disconnected()

        sleep(2)


if __name__ == '__main__':
    main()
