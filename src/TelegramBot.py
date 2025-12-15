from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import asyncio
import re

from src.LogClass import AsynLogClass

class TelegramBot:
    def __init__(self, token, chat_id=None):
        self.app = ApplicationBuilder().token(token=token).post_init(self.post_init).build()
        self.app.add_handler(CommandHandler('connect_to_user', self.connect_user))
        self.app.add_handler(CommandHandler('reload_user', self.reload_user))
        self.app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.responce))
        self.app.add_handler(CommandHandler('otvet', self.responce))

        self.chat_id = chat_id
        self.responce_text: str = "Nothing"

        self.event_loop = None
        self.log_file = AsynLogClass()

    async def post_init(self, application):
        self.event_loop = asyncio.get_running_loop()

    async def send_message(self, message:str):
        if self.chat_id:
            await self.app.bot.send_message(chat_id=self.chat_id, text=message)

    async def connect_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self.chat_id:
            self.chat_id = update.effective_chat.id
            await context.bot.send_message(chat_id=self.chat_id, text="Connect to user? Successfully")
            await self.log_file.rename("connect user")

    async def reload_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.id == self.chat_id:
            self.chat_id = None
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Reload to user? Successfully")
            await self.log_file.rename("disconnect user")

    async def responce(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.id == self.chat_id:
            text = await asyncio.to_thread(self.sanitize_text, update.message.text)
            self.responce_text = text
            await self.log_file.rename(text)

    def send_text(self, message: str):
        if self.event_loop and self.event_loop.is_running():
            asyncio.run_coroutine_threadsafe(
                self.send_message(message),
                self.event_loop
            )

    def get_text(self):
        return self.responce_text

    def stop(self):
        asyncio.run(
           self.log_file.stop()
        )
        if self.event_loop and self.event_loop.is_running():
            asyncio.run_coroutine_threadsafe(
                self.app.stop(),
                self.event_loop
            )

    def get_last_user_id(self):
        return self.chat_id

    def start(self):
        self.app.run_polling()

    def sanitize_text(self, text:str) -> str:

        text = text.replace("/otvet", "")

        text = re.sub(r"[^A-Za-z\u0400-\u04FF0-9\s]+", "", text)
        text = re.sub(r"\s+", " ", text).strip()

        return text
