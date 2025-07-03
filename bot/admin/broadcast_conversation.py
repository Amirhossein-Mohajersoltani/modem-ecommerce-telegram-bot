from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from database import *
from utils import *


database = Database()


GET_MESSAGE = 1


async def start_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not database.is_admin(update.effective_user.id) or database.is_owner(update.effective_user.id):
        return ConversationHandler.END

    context.user_data.clear()
    context.user_data["broadcast"] = True

    reply_markup = create_break_button()
    await update.message.reply_text("لطفاً پیام مورد نظر برای ارسال گروهی را وارد کنید:", reply_markup=reply_markup)
    return GET_MESSAGE


async def send_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text

    if not message.strip():
        await update.message.reply_text("پیام نمی‌تواند خالی باشد. لطفاً یک پیام معتبر وارد کنید.")
        return GET_MESSAGE

    users = database.fetch_data("users")

    if not users:
        reply_markup = create_admin_panel()
        await update.message.reply_text("هیچ کاربری پیدا نشد.", reply_markup=reply_markup)
        return ConversationHandler.END

    success_count = 0
    failed_count = 0

    for user in users:
        chat_id = user[1]
        try:
            await context.bot.send_message(chat_id=chat_id, text=message)
            success_count += 1
        except Exception as e:
            print(f"خطا در ارسال به {chat_id}: {e}")
            failed_count += 1

    reply_markup = create_admin_panel()
    await update.message.reply_text(
        f"✅ پیام با موفقیت ارسال شد.\n"
        f"🟢 موفق: {success_count} نفر\n"
        f"🔴 ناموفق: {failed_count} نفر"
        , reply_markup=reply_markup
    )
    return ConversationHandler.END


def broadcast_conv_handler():
    broadcast_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & filters.Regex(r'^ارسال پیام گروهی$'), start_broadcast)],
        states={
            GET_MESSAGE: [
                MessageHandler(filters.TEXT & filters.Regex(r'^ارسال پیام گروهی$'), start_broadcast),
                MessageHandler(filters.Regex("^لغو عملیات!$"), admin_owner_panel_break_conversation),
                MessageHandler(filters.TEXT & ~filters.COMMAND, send_broadcast)
            ]
        },
        fallbacks=[CommandHandler('done', user_panel_break_conversation)],
    )
    return broadcast_handler