from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, CallbackQueryHandler, CommandHandler, filters
from database import *
from utils import *


database = Database()

# States
UPDATE_USER_SHOW_OPTIONS, UPDATE_CONVERSATION_CONTROL = range(2)

# Start Point
async def update_user_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not database.is_contain(update.effective_chat.id, "users", f"chat_id = {update.effective_chat.id}"):
        return ConversationHandler.END

    context.user_data.clear()
    context.user_data['update_user_info_conv'] = True


    context.user_data["id"] = update.effective_chat.id
    context.user_data["username"] = None
    context.user_data["phone"] = None
    context.user_data["address"] = None
    return await update_user_show_options(update, context)

# UPDATE_USER_SHOW_OPTIONS
async def update_user_show_options(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if (context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get("update_record")
            or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user') or context.user_data.get('add_owner')):
        return ConversationHandler.END

    if context.user_data.get('payment_conv') or context.user_data.get('simcard_conv') or context.user_data.get(
            'modem_conv'):
        return ConversationHandler.END


    # Get Different Types of Input
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        data = query.data
    elif update.message:
        message = update.message.text

    text = "لطفا یکی از موارد زیر را انتخاب کنید:"

    # Set Username
    if context.user_data.get("set") == "username":
        if not is_valid_name(message):
            await update.message.reply_text("❌ نام وارد شده نامعتبر است! لطفا فقط از حروف فارسی یا لاتین استفاده کنید:")
            return UPDATE_USER_SHOW_OPTIONS

        context.user_data["username"] = message
        text = "نام شما دریافت شد درصورت اتمام کار لطفا بر روی دکمه ویرایش کلیک کنید درغیر این صورت " + text

    # Set Phone
    elif context.user_data.get("set") == "phone":
        user_input = convert_numbers(message).strip()

        if not is_valid_phone(user_input):
            await update.message.reply_text(
                "❌ شماره تماس نامعتبر است! لطفا شماره‌ای ۱۱ رقمی که با ۰۹ شروع می‌شود، وارد کنید:")
            return UPDATE_USER_SHOW_OPTIONS


        context.user_data["phone"] = user_input
        text = "شماره تماس شما دریافت شد درصورت اتمام کار لطفا بر روی دکمه ویرایش کلیک کنید درغیر این صورت " + text

    # Set Address
    elif context.user_data.get("set") == "address":
        if not is_valid_address(message):
            await update.message.reply_text("❌ آدرس خیلی کوتاه است! لطفا یک آدرس کامل وارد کنید:")
            return UPDATE_USER_SHOW_OPTIONS

        context.user_data["address"] = message
        text = "آدرس شما دریافت شد درصورت اتمام کار لطفا بر روی دکمه ویرایش کلیک کنید درغیر این صورت " + text

    keyboard_options = [
        [
            InlineKeyboardButton(text="ویرایش نام", callback_data="username -uu"),
            InlineKeyboardButton(text="ویرایش شماره تماس", callback_data="phone -uu")
        ],
        [
            InlineKeyboardButton(text="ویرایش آدرس", callback_data="address -uu")
        ],
        [
            InlineKeyboardButton(text="ویرایش", callback_data="edit -uu")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard_options)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text,reply_markup=reply_markup)
    return UPDATE_CONVERSATION_CONTROL


# UPDATE_CONVERSATION_CONTROL

# UPDATE_USERNAME
async def update_username(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if (context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get("update_record")
            or context.user_data.get('add_admin') or context.user_data.get(
                'delete_user') or context.user_data.get('add_owner')):
        return ConversationHandler.END
    # singular conv checker
    if context.user_data.get('payment_conv') or context.user_data.get('simcard_conv') or context.user_data.get('modem_conv'):
        return ConversationHandler.END

    await context.bot.send_message(chat_id=update.effective_chat.id, text="لطفا نام و نام خانوادگی خود را وارد کنید:")
    context.user_data["set"] = "username"

    return UPDATE_USER_SHOW_OPTIONS


# UPDATE_PHONE
async def update_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if (context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get("update_record")
            or context.user_data.get('add_admin') or context.user_data.get(
                'delete_user') or context.user_data.get('add_owner')):
        return ConversationHandler.END
    # singular conv checker
    if context.user_data.get('payment_conv') or context.user_data.get('simcard_conv') or context.user_data.get('modem_conv'):
        return ConversationHandler.END

    await context.bot.send_message(chat_id=update.effective_chat.id, text="لطفا شماره تماس خود را وارد کنید:")
    context.user_data["set"] = "phone"

    return UPDATE_USER_SHOW_OPTIONS


# UPDATE_ADDRESS
async def update_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if (context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get("update_record")
            or context.user_data.get('add_admin') or context.user_data.get(
                'delete_user') or context.user_data.get('add_owner')):
        return ConversationHandler.END
    # singular conv checker
    if context.user_data.get('payment_conv') or context.user_data.get('simcard_conv') or context.user_data.get('modem_conv'):
        return ConversationHandler.END

    await context.bot.send_message(chat_id=update.effective_chat.id, text="لطفا آدرس پستی خود را وارد کنید:")
    context.user_data["set"] = "address"

    return UPDATE_USER_SHOW_OPTIONS


# UPDATE_USER
async def update_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if (context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get("update_record")
            or context.user_data.get('add_admin') or context.user_data.get(
                'delete_user') or context.user_data.get('add_owner')):
        return ConversationHandler.END
    # singular conv checker
    if context.user_data.get('payment_conv') or context.user_data.get('simcard_conv') or context.user_data.get('modem_conv'):
        return ConversationHandler.END

    record = Record(
        table_name="users",
        username= context.user_data["username"],
        phone= context.user_data["phone"],
        address=context.user_data["address"],
    )
    if database.update_record(record, condition=f"chat_id = '{context.user_data["id"]}'"):
        text = "عملیات با موفقیت انجام شد."
    else:
        text = "مشکلی در اضافه کردن رکورد به وجود آمده است!"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    context.user_data.clear()
    return ConversationHandler.END




# Handler
def update_user_handler():

    update_user_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^ویرایش اطلاعات من$"), update_user_start)],
        states={
            UPDATE_USER_SHOW_OPTIONS: [
                CallbackQueryHandler(update_user_show_options),
                MessageHandler(filters.TEXT & ~filters.COMMAND, update_user_show_options)
            ],
            UPDATE_CONVERSATION_CONTROL: [
                CallbackQueryHandler(update_username, pattern="^username -uu$"),
                CallbackQueryHandler(update_phone, pattern="^phone -uu$"),
                CallbackQueryHandler(update_address, pattern="^address -uu$"),
                CallbackQueryHandler(update_user, pattern="^edit -uu$")
            ]
        },
        fallbacks=[CommandHandler('done', break_conversation)]
    )
    return update_user_conv_handler