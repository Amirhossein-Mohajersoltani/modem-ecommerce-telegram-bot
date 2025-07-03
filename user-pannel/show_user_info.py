from telegram import Update
from telegram.ext import  ContextTypes
from database import *
from utils import *


database = Database()



async def show_user_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not database.is_contain(update.effective_chat.id, "users", f"chat_id = {update.effective_chat.id}"):
        return ConversationHandler.END

    user_data = database.fetch_data(table_name="users",condition=f"chat_id = '{update.effective_chat.id}'")

    full_name = user_data[0][2] if user_data[0][2] else "نامی یافت نشد"
    phone = user_data[0][4] if user_data[0][4] else "شماره تماسی یافت نشد"
    address = user_data[0][5] if user_data[0][5] else "آدرسی یافت نشد"

    additional_data = {
        "{full_name}": full_name,
        "{phone}": phone,
        "{address}": address
    }
    text = get_dynamic_text("modem", "modem_model_options_buy", "model_options", additional_data=additional_data)


    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)