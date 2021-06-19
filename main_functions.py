import re
import asyncio

from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
from telethon import TelegramClient, events
from telethon.events.common import EventCommon
import secret_constants

channel_id = -1001278933699
client: TelegramClient = None
channel_entity = None


# -------------------------------- BOT --------------------------------
def start_handler(update: Update, _):
    if update.message.chat_id == secret_constants.master_id or update.message.from_user.id == secret_constants.master_id:
        update.message.reply_text("Senpai!\n/reload\n/shutdown")
    elif update.message.chat_id == secret_constants.cutie_id or update.message.from_user.id == secret_constants.cutie_id:
        update.message.reply_text("Мяу 😻")
    else:
        update.message.reply_text("Тебе здесь не рады, кожаный мешок!!")


def bite_handler(update: Update, context: CallbackContext):
    if update.message.chat_id == secret_constants.master_id or update.message.from_user.id == secret_constants.master_id:
        context.bot.send_message(secret_constants.cutie_id, update.message.text)
    elif update.message.chat_id == secret_constants.cutie_id or update.message.from_user.id == secret_constants.cutie_id:
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
                                    chats=[secret_constants.cutie_id, channel_id, -1001444301389, -1001282562260],
                                    outgoing=True)


async def handler_goodnight(event: EventCommon):
    send_to = {secret_constants.cutie_id: 'Данночка', channel_id: 'подписчики', -1001444301389: 'чатик', -1001282562260: 'чатик'}
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


event_media_to_forward = events.NewMessage(func=lambda e: e.chat_id in [-1001444301389, -1001282562260])


async def handler_media_to_forward(event: events.NewMessage):
    fields = ['audio', 'document', 'file', 'photo', 'video', 'video_note', 'voice']
    for field in fields:
        if getattr(event.message, field) is not None:
            print("Forward", field)
            await client.forward_messages(await client.get_entity(-1001490096533), event.message)
            # await event.message.forward_to(channel_entity)
            break


def get_user_handlers() -> dict:
    return {
        event_goodnight: handler_goodnight,
        event_media_to_forward: handler_media_to_forward
    }


# --------------------------------------------- SERVICE ----------------------------------------------
def init_state():
    pass


def save_state(to_json=False) -> dict:
    if to_json:
        return {}
    else:
        return {
            'channel_entity': channel_entity
        }


def load_state(state: dict, _client: TelegramClient):
    global client
    global channel_entity
    client = _client
    if 'channel_entity' in state:
        channel_entity = state['channel_entity']
    else:
        with client:
            channel_entity = client.get_entity(-1001490096533)
