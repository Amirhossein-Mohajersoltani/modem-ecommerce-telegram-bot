from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telegram.ext import ConversationHandler, ContextTypes, MessageHandler, filters, CommandHandler, \
    CallbackQueryHandler
from random import randint,choice,shuffle
from database import *
from utils import *

available_tokens = []

database = Database()


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


    password_letters = [choice(letters) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    return password


async def gen_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if database.is_admin(update.effective_chat.id) or database.is_owner(update.effective_user.id):
        token_link = generate_password()
        link = "https://t.me/IranModemBot?start=" + token_link
        available_tokens.append(token_link)

        await context.bot.send_message(chat_id=update.effective_chat.id, text=link)

