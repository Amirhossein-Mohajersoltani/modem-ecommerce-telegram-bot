from telegram import Update
from telegram.ext import ConversationHandler, ContextTypes, MessageHandler, filters, CommandHandler
from database import *
from utils import *

database = Database()

# States
DELETE_ADMIN_BY_ID = range(1)


async def delete_admin_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask admin to enter new an id"""
    # Check is user admin or not
    if database.is_owner(update.effective_chat.id):
        context.user_data.clear()
        context.user_data["delete_admin"] = True

        # create break conversation button
        break_button = create_break_button()

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="لطفا آیدی ادمین را ارسال کنید:",
            reply_markup=break_button
        )
        return DELETE_ADMIN_BY_ID
    return ConversationHandler.END



# DELETE_ADMIN_BY_ID
async def delete_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    if not is_valid_number(user_input):
        text = "آیدی تنها شامل اعداد صحیح غیر صفر می باشد.\nلطفا دوباره آیدی را ارسال کنید:"
        await update.message.reply_text(text)
        return DELETE_ADMIN_BY_ID


    admin_id = int(user_input)
    # creat panel
    reply_markup = create_owner_panel()

    # Check if id exists in database or not
    if database.is_contain(value=admin_id, table_name="users", condition=f"id = {admin_id}"):

        # Check if the process done successfully or not
        if database.update_record(Record(table_name="users",is_admin=False),condition=f"id = {admin_id}"):
            text="عملیات با موفقیت انجام شد."
        else:
            text="عملیات انجام نشد!"

    else:
        text="آیدی در لیست موجود نمی باشد!"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text,reply_markup=reply_markup)
    return ConversationHandler.END


# Handler
def delete_admin_handler():
    delete_admin_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^حذف ادمین$"), delete_admin_button)],
        states={
            DELETE_ADMIN_BY_ID: [
                MessageHandler(filters.Regex("^حذف ادمین$"), delete_admin_button),
                MessageHandler(filters.Regex("^لغو عملیات!$"), owner_panel_break_conversation),
                MessageHandler(filters.TEXT & (~filters.COMMAND), delete_admin),
            ],
        },
        fallbacks=[CommandHandler('done', owner_panel_break_conversation)],
    )
    return delete_admin_conv_handler