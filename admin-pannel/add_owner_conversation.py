from telegram import Update
from telegram.ext import ConversationHandler, ContextTypes, MessageHandler, filters, CommandHandler
from database import *
from utils import *

database = Database()

# States
ADD_OWNER_BY_ID = range(1)


# Start Point
async def add_owner_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask admin to enter new admin id"""
    # Check if user admin?
    if database.is_owner(update.effective_chat.id):
        context.user_data.clear()
        context.user_data["add_owner"] = True


        reply_markup = create_break_button()
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="لطفا آیدی مالک جدید را ارسال کنید:",
            reply_markup=reply_markup
        )
        return ADD_OWNER_BY_ID
    return ConversationHandler.END


# ADD_OWNER_BY_ID
async def add_owner_by_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save new admin id and promote them to admin"""
    # active one conversation per moment
    if context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get("update_record") or context.user_data.get(
        'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user'):
        return ConversationHandler.END

    # Check user input contain only numbers

    user_input = convert_numbers(update.message.text).strip()

    if not is_valid_number(user_input):
        text = "آیدی تنها شامل اعداد صحیح غیر صفر می باشد.\nلطفا دوباره آیدی را ارسال کنید:"
        await update.message.reply_text(text)
        return ADD_OWNER_BY_ID

    owner_id = int(user_input)
    if not database.is_contain(owner_id, "users", f" id = {owner_id}"):
        text = "مقدار آیدی معتبر نمی باشد.\nلطفا دوباره آیدی را ارسال کنید:"
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
        )
        # Ask to enter again before continue
        return ADD_OWNER_BY_ID

    # Save id

    # creat panel
    reply_markup = create_owner_panel()

    # Check if id exists in database or not
    if database.is_contain(owner_id, "users", f"id = {owner_id}"):

        # Check if the process done successfully or not
        if database.update_record(Record(table_name="users", is_owner=True), condition=f"id = {owner_id}"):
            text = "عملیات با موفقیت انجام شد."
            result = database.fetch_data("users", f"id = {owner_id}")
            new_owner_chat_id = result[0][1]
            owner_reply_markup = create_owner_panel()
            await context.bot.send_message(chat_id=new_owner_chat_id, text="شما به مالک ارتقا یافتید.",
                                           reply_markup=owner_reply_markup)
        else:
            text = "عملیات اضافه انجام نشد!"

    else:
        text = "آیدی در لیست موجود نمی باشد!"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
    # Conversation Finished
    return ConversationHandler.END


# Handler
def add_owner_handler():
    add_owner_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^ارتقا ادمین به مالک$"), add_owner_button)],
        states={
            ADD_OWNER_BY_ID: [
                MessageHandler(filters.Regex("^ارتقا ادمین به مالک$"), add_owner_button),
                MessageHandler(filters.Regex("^لغو عملیات!$"), admin_owner_panel_break_conversation),
                MessageHandler(filters.TEXT & (~filters.COMMAND), add_owner_by_id)
            ],
        },
        fallbacks=[CommandHandler('done', owner_panel_break_conversation)],
    )
    return add_owner_conv_handler