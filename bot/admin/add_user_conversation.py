from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler, CommandHandler, MessageHandler, \
    filters
from database import *

from utils import *

database = Database()

# States
GET_USER_INFO , SIGN_UP_USER = range(2)


# Start Point
async def get_username(update:Update, context: ContextTypes.DEFAULT_TYPE):
    # save chat id
    context.user_data["chat_id"] = update.effective_chat.id

    text= "لطفا نام و نام خانوادگی خود را وارد کنید:"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    return GET_USER_INFO



# GET_USER_INFO
async def get_user_info(update:Update, context: ContextTypes.DEFAULT_TYPE):
    # save full name
    context.user_data["full_name"] = update.message.text
    text = "لطفا شماره تماس خود را وارد کنید:"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    return SIGN_UP_USER



async def sign_up_user(update:Update, context: ContextTypes.DEFAULT_TYPE):
    phone_number = update.message.text.strip()

    # Check Validation
    if len(phone_number) != 11 or not phone_number.isdigit():
        text = "شماره تماس معتبر نمی باشد!\n لطفا مجدد شماره تماس خود را ارسال کنید:"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return SIGN_UP_USER

    # Check if signing up user was successful
    if database.add_record(Record(table_name="users", chat_id=context.user_data["chat_id"], phone=phone_number,
                                  username=context.user_data["full_name"])):
        reply_markup = create_user_panel()
        text = "به ربات فروش مودم و سیمکارت ارتباطات نوین خوش آمدید\n\nدرصورتی که سوال و یا احتیاج به راهنمایی داشتید، می توانید از طریق پشتیبانی ما را درجریان مشکل خود قرار بدهید:\n@ID_Test"
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            reply_markup=reply_markup,
            text=text
        )
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,text="مشکلی در ورود کاربران جدید پیش آمده. لطفا مشکل را با پشتیبانی درمیان بگذارید.")

    return ConversationHandler.END


# Handler
def add_user_handler():
    add_user_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(get_username, pattern="^register$")],
        states={
            GET_USER_INFO: [
                MessageHandler(filters.TEXT & (~filters.COMMAND), get_user_info),
            ],
            SIGN_UP_USER: [
                MessageHandler(filters.TEXT & (~filters.COMMAND), sign_up_user),
            ],
        },
        fallbacks=[CommandHandler('done', break_conversation)],
    )

    return add_user_conv_handler