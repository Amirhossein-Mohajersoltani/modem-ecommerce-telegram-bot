from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CommandHandler, \
    CallbackQueryHandler
from database import *
from utils import *
database = Database()


# States
DELETE_GET_PRODUCT_ID, DELETE_PRODUCT = range(2)

async def delete_record_button(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # Check user is admin ot not
    if database.is_admin(update.effective_chat.id) or database.is_owner(update.effective_chat.id):
        context.user_data.clear()
        context.user_data["delete_product"] = True


        keyboard = [
            [
                InlineKeyboardButton("مودم", callback_data="modem -dp"),
                InlineKeyboardButton(text="سیمکارت", callback_data="simcard -dp"),
            ],
            ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        text = "لطفا یکی از گزینه های زیر را انتخاب کنید:"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
        return DELETE_GET_PRODUCT_ID
    return ConversationHandler.END



#  DELETE_GET_PRODUCT_ID
async def delete_get_product_id(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if (context.user_data.get("add_product") or context.user_data.get("delete_admin")
        or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get("update_record") or context.user_data.get(
        'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user') or context.user_data.get('add_owner')):
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()
    context.user_data["table_name"] = query.data.split()[0]


    reply_markup = create_break_button()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="لطفا آیدی محصول را وارد کنید.", reply_markup=reply_markup)

    return DELETE_PRODUCT



# DELETE_PRODUCT
async def delete_product(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if (context.user_data.get("add_product") or context.user_data.get("delete_admin")
            or context.user_data.get("dynamic_text") or context.user_data.get(
                "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
                "show_product") or context.user_data.get("update_record") or context.user_data.get(
                'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
                'delete_user') or context.user_data.get('add_owner')):
        return ConversationHandler.END

    user_input = convert_numbers(update.message.text).strip()

    if not is_valid_number(user_input):
        text = "آیدی تنها شامل اعداد صحیح غیر صفر می باشد.\nلطفا دوباره آیدی را ارسال کنید:"
        await update.message.reply_text(text)
        return DELETE_PRODUCT



    admin_id = int(user_input)
    if not database.is_contain(admin_id, context.user_data["table_name"], f" id = {admin_id}"):
        text = "مقدار آیدی معتبر نمی باشد.\nلطفا دوباره آیدی را ارسال کنید:"
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
        )
        # Ask to enter again before continue
        return DELETE_PRODUCT

    if database.delete_record(context.user_data["table_name"],f"id = {admin_id}"):
        text = "عملیات با موفقیت انجام شد."
    else:
        text = "عملیات با خطا مواجه شد."

    if database.is_owner(update.effective_chat.id):
        reply_markup = create_owner_panel()
    elif database.is_admin(update.effective_chat.id):
        reply_markup = create_admin_panel()
    await context.bot.send_message(chat_id=update.effective_chat.id,text=text,reply_markup=reply_markup)
    return ConversationHandler.END



# Handler
def delete_product_handler():
    delete_product_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^حذف محصول$"), delete_record_button)],
        states={
            DELETE_GET_PRODUCT_ID: [
                MessageHandler(filters.Regex("^لغو عملیات!$"), admin_owner_panel_break_conversation),
                MessageHandler(filters.Regex("^حذف محصول$"), delete_record_button),
                CallbackQueryHandler(delete_get_product_id, pattern=r"^(modem|simcard) -dp$"),
            ],
            DELETE_PRODUCT: [
                MessageHandler(filters.Regex("^حذف محصول$"), delete_record_button),
                MessageHandler(filters.Regex("^لغو عملیات!$"), admin_owner_panel_break_conversation),
                MessageHandler(filters.TEXT & (~filters.COMMAND), delete_product)
            ]
        },
        fallbacks=[CommandHandler('done', admin_owner_panel_break_conversation)],
    )
    return delete_product_conv_handler