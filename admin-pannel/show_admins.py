from telegram import Update
from telegram.ext import  ContextTypes
from database import *
from utils import *


database = Database()


async def show_admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if database.is_admin(update.effective_chat.id) or database.is_owner(update.effective_chat.id):
        result = database.fetch_data("users", "is_admin = 1")
        text = show_admin_admins_users(result)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)