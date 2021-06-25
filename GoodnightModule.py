from telethon import events

from BaseModule import *
import config_file


class GoodnightModule(BaseModule):
    def __init__(self, client: TelegramClient):
        super().__init__(client)
        self.event_goodnight = events.NewMessage(func=self.goodnight_filter,
                                                 chats=[config_file.cutie_id, config_file.channel_id,
                                                        -1001444301389, -1001282562260],
                                                 outgoing=True)

    def get_user_handlers(self) -> dict:
        return {
            self.event_goodnight: self.goodnight_handler
        }

    @staticmethod
    def goodnight_filter(event):
        return event.message.photo is not None and (
                event.message.text.startswith('Утречка') or event.message.text.startswith('Спокойной ночи')
        )

    async def goodnight_handler(self, event):
        send_to = {config_file.cutie_id: 'Данночка', config_file.channel_id: 'подписчики',
                   -1001444301389: 'чатик', -1001282562260: 'чатик'}
        text = event.message.text
        if text.endswith(', чатик'):
            text = text[:text.rfind(', ')]
        for recv in send_to:
            if event.chat_id != recv:
                if text.startswith('Спокойной ночи'):
                    text_ = text + ', ' + send_to[recv]
                else:
                    text_ = text
                await self.client.send_message(recv, text_, file=event.message.photo)


module = GoodnightModule
