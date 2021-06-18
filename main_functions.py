import re

from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
from telethon import TelegramClient, events
from telethon.events.common import EventCommon
import secret_constants

cutie_id = 511196942
channel_id = -1001278933699
client: TelegramClient = None


# -------------------------------- BOT --------------------------------
def start_handler(update: Update, _):
    if update.message.chat_id == secret_constants.master_id or update.message.from_user.id == secret_constants.master_id:
        update.message.reply_text("Senpai!\n/reload\n/shutdown")
    elif update.message.chat_id == cutie_id or update.message.from_user.id == cutie_id:
        update.message.reply_text("Мяу 😻")
    else:
        update.message.reply_text("Тебе здесь не рады, кожаный мешок!!")


def bite_handler(update: Update, context: CallbackContext):
    if update.message.chat_id == secret_constants.master_id or update.message.from_user.id == secret_constants.master_id:
        context.bot.send_message(cutie_id, update.message.text)
    elif update.message.chat_id == cutie_id or update.message.from_user.id == cutie_id:
        context.bot.send_message(secret_constants.master_id, update.message.text)
    context.bot.send_message(secret_constants.master_id, str(update.message.chat_id))


def get_handlers() -> list:
    return [
        CommandHandler('start', start_handler),
        MessageHandler(Filters.regex(re.compile('Кусь.*', re.IGNORECASE)), bite_handler),
    ]


# -------------------------------- USER ----------------------------
event_goodnight = events.NewMessage(func=lambda e: e.message.photo is not None
                                                   and (e.message.text.startswith('Утречка')
                                                        or e.message.text.startswith('Спокойной ночи')),
                                    chats=[cutie_id, channel_id, -1001444301389, -1001282562260],
                                    outgoing=True)


async def handler_goodnight(event: EventCommon):
    send_to = {cutie_id: 'Данночка', channel_id: 'читатели', -1001444301389: 'чатик', -1001282562260: 'чатик'}
    text = event.message.text
    if text.endswith(', чатик'):
        text = text[:text.rfind(', ')]
    for recv in send_to:
        if event.chat_id != recv:
            if text.startswith('Спокойной ночи'):
                text_ = text + ', ' + send_to[recv]
            else:
                text_ = text
            await client.send_message(recv, text_, file=event.message.photo)


def get_user_handlers() -> dict:
    return {
        event_goodnight: handler_goodnight
    }


# with TelegramClient('name', api_id, api_hash) as client:
#     channel_entity = client.get_entity(-1001490096533)
#
#     # @client.on(events.MessageDeleted)
#     # async def handler_del(event):
#     #     # Log all deleted message IDs
#     #     for msg_id in event.deleted_ids:
#     #         print('Message', msg_id, 'was deleted in', event.chat_id)
#
#     @client.on(events.NewMessage(func=lambda e: e.chat_id in [-1001444301389, -1001282562260]))
#     async def handler_new(event: events):
#         fields = ['audio', 'document', 'file', 'photo', 'video', 'video_note', 'voice']
#         for field in fields:
#             if getattr(event.message, field) is not None:
#                 print("Forward", field)
#                 await event.message.forward_to(channel_entity)
#                 break
#
#
#     @client.on(events.NewMessage())
#     async def handler_new(event):
#         print(event.chat.title, event.chat.username, event.chat_id)
#
#     print("Start")
#
#     client.run_until_disconnected()


# --------------------------------------------- SERVICE ----------------------------------------------
def init_state():
    pass


def save_state(to_json=False) -> dict:
    return {}


def load_state(state: dict, _client: TelegramClient):
    global client
    client = _client
