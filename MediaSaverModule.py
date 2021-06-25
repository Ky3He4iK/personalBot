from telethon import events

from BaseModule import *


class MediaSaverModule(BaseModule):
    def __init__(self, client: TelegramClient):
        super().__init__(client)
        self.event_media_saver = events.NewMessage(func=lambda e: e.chat_id in [-1001444301389, -1001282562260])

    def get_user_handlers(self) -> dict:
        return {
            self.event_media_saver: self.media_saver_handler
        }

    @staticmethod
    def goodnight_filter(event):
        return event.message.photo is not None and (
                event.message.text.startswith('Утречка') or event.message.text.startswith('Спокойной ночи')
        )

    async def media_saver_handler(self, event: events.NewMessage):
        fields = ['audio', 'document', 'file', 'photo', 'video', 'video_note', 'voice']
        for field in fields:
            if getattr(event.message, field) is not None:
                print("Forward", field)
                await self.client.forward_messages(await self.client.get_entity(-1001490096533), event.message)
                break


module = MediaSaverModule
