from telegram import Update
from telegram.ext import ConversationHandler, ContextTypes, MessageHandler, filters, CommandHandler
from database import *
from utils import *


# States
EDIT_CARD = range(1)

database = Database()

# Start Point
async def edit_card_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask owner to enter new card number"""
    # Check is user admin or not
    if database.is_owner(update.effective_chat.id):
        context.user_data.clear()

        # create break conversation button
        break_button = create_break_button()

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="لطفا شماره کارت جدید را ارسال کنید:",
            reply_markup=break_button
        )
        return EDIT_CARD
    return ConversationHandler.END



# EDIT_CARD
async def edit_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save new admin id and disprove them to admin"""
    # active one conversation per moment
    if context.user_data.get("add_product") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get("update_record") or context.user_data.get(
        'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user') or context.user_data.get('add_owner'):
        return ConversationHandler.END


    # Check user input contain only numbers
    user_input = convert_numbers(update.message.text).strip()

    if not user_input.isdigit() and len(user_input) != 16:
        text = "شماره کارت معتبر نمی باشد.\nلطفا دوباره شماره کارت را ارسال کنید:"
        await update.message.reply_text(text)
        return EDIT_CARD


    import payment
    payment.CARD_NUMBER = user_input

    # creat panel
    reply_markup = create_owner_panel()
    text="عملیات با موفقیت انجام شد."


    await context.bot.send_message(chat_id=update.effective_chat.id, text=text,reply_markup=reply_markup)
    return ConversationHandler.END


# Handler
def edit_card_handler():
    return ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^ویرایش شماره کارت$"), edit_card_start)],
        states={
            EDIT_CARD: [
                MessageHandler(filters.Regex("^ویرایش شماره کارت$"), edit_card_start),
                MessageHandler(filters.Regex("^لغو عملیات!$"), owner_panel_break_conversation),
                MessageHandler(filters.TEXT & ~filters.COMMAND, edit_card),
            ],
        },
        fallbacks=[CommandHandler('done', owner_panel_break_conversation)],
    )
