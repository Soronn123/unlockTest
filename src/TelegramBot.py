from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import asyncio

from src.LogClass import AsynLogClass

class TelegramBot:
    def __init__(self, token, chat_id=None):
        self.app = ApplicationBuilder().token(token=token).post_init(self.post_init).build()
        self.app.add_handler(CommandHandler('connect_to_user', self.connect_user))
        self.app.add_handler(CommandHandler('reload_user', self.reload_user))
        self.app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.responce))
        self.app.add_handler(CommandHandler('otvet', self.responce_command))
        self.app.add_handler(CommandHandler('question', self.send_message))

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

    async def reload_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.chat_id = update.effective_chat.id
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Reload to user? Successfully")

    async def responce(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.id == self.chat_id:
            self.responce_text = update.message.text
            self.log_file.rename(update.message.text)

    async def responce_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.responce(update, context)

    async def responce_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.responce(update, context)

    def send_text(self, message: str):
        if self.event_loop and self.event_loop.is_running():
            asyncio.run_coroutine_threadsafe(
                self.send_message(message),
                self.event_loop
            )

    def get_text(self):
        return self.responce_text

    def stop(self):
        self.log_file.stop()
        if self.event_loop and self.event_loop.is_running():
            asyncio.run_coroutine_threadsafe(
                self.app.stop(),
                self.event_loop
            )

    def start(self):
        self.app.run_polling()
