from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, CallbackQueryHandler, filters, \
    CommandHandler
from database import *
from utils import *

database = Database()


ADD_PRODUCT_MODEL, ADD_PRODUCT_NAME, ADD_PRODUCT_PRICE, ADD_PRODUCT_COUNT, ADD_PRODUCT_DESCRIPTION, ADD_PRODUCT_SITUATION, ADD_PRODUCT_IMAGE_ID, ADD_PRODUCT = range(8)


# Start Point
async def add_product_button(update:Update, context:ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["add_product"] = True

    # Check is user admin or not
    if database.is_admin(update.effective_chat.id) or database.is_owner(update.effective_chat.id):




        keyboard = [
            [
                InlineKeyboardButton("مودم", callback_data="modem -ap"),
                InlineKeyboardButton(text="سیمکارت", callback_data="simcard -ap"),
            ],
        ]


        reply_markup = InlineKeyboardMarkup(keyboard)

        text = "لطفا یکی از گزینه های زیر را انتخاب کنید:"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
        return ADD_PRODUCT_MODEL

    return ConversationHandler.END



# ADD_PRODUCT_MODEL
async def add_product_model(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
            "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
            "show_product") or context.user_data.get("update_record") or context.user_data.get(
            'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
            'delete_user') or context.user_data.get('add_owner'):
        return ConversationHandler.END

    # Table name were determined and set
    query = update.callback_query
    await query.answer()
    context.user_data["table_name"] = query.data.split()[0]

    # create keyboard
    keyboard = [
        [
            InlineKeyboardButton("5G", callback_data="5G -ap"),
        ],
        [
            InlineKeyboardButton("TD-LTE", callback_data="TD-LTE -ap"),
        ],
        [
            InlineKeyboardButton("4G", callback_data="4G -ap"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)


    text = "لطفا مدل محصول را انتخاب کنید:"
    await query.edit_message_text(text=text, reply_markup=reply_markup)
    return ADD_PRODUCT_NAME



# ADD_PRODUCT_NAME
async def add_product_name(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get("update_record") or context.user_data.get(
        'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user') or context.user_data.get('add_owner'):
        return ConversationHandler.END

    # Save Product Model
    query = update.callback_query
    await query.answer()
    context.user_data["model"] = query.data.split()[0]


    text = "لطفا یک نام برای محصول وارد کنید.\nاز این نام برای معرفی محصول به کاربر استفاده می شود."

    reply_markup = create_break_button()

    await query.message.reply_text(text=text, reply_markup=reply_markup)
    return ADD_PRODUCT_PRICE



# ADD_PRODUCT_PRICE
async def add_product_price(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get("update_record") or context.user_data.get(
        'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user') or context.user_data.get('add_owner'):
        return ConversationHandler.END

    # Save Product Name
    name = update.message.text
    context.user_data["name"] = name

    text = "لطفا قیمت محصول را وارد کنید:"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    return ADD_PRODUCT_COUNT



# ADD_PRODUCT_COUNT
async def add_product_count(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get("update_record") or context.user_data.get(
        'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user') or context.user_data.get('add_owner'):
        return ConversationHandler.END

    # Determine the product count
    user_input = convert_numbers(update.message.text).strip()

    if not is_valid_number(user_input):
        text = "قیمت وارد شده معتبر نمی باشد\nلطفا مجددا قیمت محصول را وارد کنید:"
        await update.message.reply_text(text)
        return ADD_PRODUCT_COUNT



    # save price
    price = int(user_input)
    context.user_data["price"] = price

    text = "لطفا میزان موجودی را وارد کنید:"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    return ADD_PRODUCT_DESCRIPTION



# ADD_PRODUCT_DESCRIPTION
async def add_product_description(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get("update_record") or context.user_data.get(
        'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user') or context.user_data.get('add_owner'):
        return ConversationHandler.END

    # Determine the order count
    user_input = convert_numbers(update.message.text).strip()

    if not is_valid_number(user_input) and not (user_input.isdigit() and int(user_input) >= 0):
        text = "مقدار وارد شده صحیح نیست. تعداد محصول باید یک عدد صحیح مثبت باشد.\nلطفا مجدد تعداد را وارد کنید:"
        await update.message.reply_text(text)
        return ADD_PRODUCT_DESCRIPTION



    # save count
    count = int(user_input)
    context.user_data["count"] = count

    text = "لطفا متن توضیحات محصول را وارد کنید.\nاز این متن برای نمایش به کاربر استفاده می شود."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    if context.user_data["table_name"] == "simcard":
        return ADD_PRODUCT
    else:
        return ADD_PRODUCT_SITUATION



# ADD_PRODUCT_SITUATION
async def add_product_situation(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get("update_record") or context.user_data.get(
        'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user') or context.user_data.get('add_owner'):
        return ConversationHandler.END

    # Save Product Description
    context.user_data["description"] = update.message.text

    # Set Keyboards
    keyboard = [
        [
            InlineKeyboardButton("مودم آکبند", callback_data="True -ap"),
            InlineKeyboardButton("مودم استوک", callback_data="False -ap")
        ],
    ]
    text = "لطفا گزینه مناسب را انتخاب کنید:"
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
    return ADD_PRODUCT_IMAGE_ID



# ADD_PRODUCT_IMAGE_ID
async def add_product_image_id(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get("update_record") or context.user_data.get(
        'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user') or context.user_data.get('add_owner'):
        return ConversationHandler.END

    # Save Product Situation
    query = update.callback_query
    await query.answer()
    context.user_data["is_new"] = eval(query.data.split()[0])

    text = "لطفا درصورت وجود، عکس محصول را ارسال کنید در غیر این صورت 0 وارد کنید:"
    await query.edit_message_text(text=text)
    return ADD_PRODUCT


# ADD_PRODUCT
async def add_product(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get("update_record") or context.user_data.get(
        'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user') or context.user_data.get('add_owner'):
        return ConversationHandler.END

    # Do the process for adding simcard
    if context.user_data["table_name"] == "simcard":
        # Save Description
        context.user_data["description"] = update.message.text
        # Check if The process was successful or not
        if database.add_record(Record(
            table_name=context.user_data["table_name"],
            product_model=context.user_data["model"],
            product_description=context.user_data["description"],
            product_price=context.user_data["price"],
            product_count=context.user_data["count"],
            product_name=context.user_data["name"]
            )
        ):
            text = "عملیات با موفقیت انجام شد."
        else:
            text = "مشکلی در هنگام عملیات پیش آمده است."

        if database.is_owner(update.effective_chat.id):
            reply_markup = create_owner_panel()
        elif database.is_admin(update.effective_chat.id):
            reply_markup = create_admin_panel()
        await context.bot.send_message(chat_id=update.effective_chat.id,text=text,reply_markup=reply_markup)
        context.user_data.clear()
        return ConversationHandler.END


    # Table Name: Modem
    # Check for input Validation and save image id
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        context.user_data["image_id"] = file_id
    elif update.message.text == "0":
        context.user_data["image_id"] = "0"
    else:
        text = "لطفا مقدار معتبر وارد کنید:"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return ADD_PRODUCT

    # Check whether the transaction was successful or not
    if database.add_record(Record(
        table_name=context.user_data["table_name"],
        product_model= context.user_data["model"],
        product_description=context.user_data["description"],
        product_price=context.user_data["price"],
        product_count=context.user_data["count"],
        product_name=context.user_data["name"],
        file_id=context.user_data["image_id"],
        is_new=context.user_data["is_new"]
        )
    ):
        text= "عملیات با موفقیت انجام شد."
    else:
        text = f"مشکلی در اضافه کردن رکورد به وجود آمده است!"

    if database.is_owner(update.effective_chat.id):
        reply_markup = create_owner_panel()
    elif database.is_admin(update.effective_chat.id):
        reply_markup = create_admin_panel()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
    context.user_data.clear()
    return ConversationHandler.END


# Handler
def add_product_handler():
    add_product_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^اضافه کردن محصول$"), add_product_button)],
        states={
            ADD_PRODUCT_MODEL: [
                MessageHandler(filters.Regex("^اضافه کردن محصول$"), add_product_button),
                MessageHandler(filters.Regex("^لغو عملیات!$"), admin_owner_panel_break_conversation),
                CallbackQueryHandler(add_product_model, pattern=r"^(modem|simcard) -ap$"),
            ],
            ADD_PRODUCT_NAME: [
                MessageHandler(filters.Regex("^اضافه کردن محصول$"), add_product_button),
                MessageHandler(filters.Regex("^لغو عملیات!$"), admin_owner_panel_break_conversation),
                CallbackQueryHandler(add_product_name, pattern=r"^(4G|TD-LTE|5G) -ap$"),
            ],
            ADD_PRODUCT_PRICE: [
                MessageHandler(filters.Regex("^اضافه کردن محصول$"), add_product_button),
                MessageHandler(filters.Regex("^لغو عملیات!$"), admin_owner_panel_break_conversation),
                MessageHandler(filters.TEXT & ~filters.COMMAND, add_product_price)
            ],
            ADD_PRODUCT_COUNT: [
                MessageHandler(filters.Regex("^اضافه کردن محصول$"), add_product_button),
                MessageHandler(filters.Regex("^لغو عملیات!$"), admin_owner_panel_break_conversation),
                MessageHandler(filters.TEXT & ~filters.COMMAND, add_product_count)
            ],
            ADD_PRODUCT_DESCRIPTION: [
                MessageHandler(filters.Regex("^اضافه کردن محصول$"), add_product_button),
                MessageHandler(filters.Regex("^لغو عملیات!$"), admin_owner_panel_break_conversation),
                MessageHandler(filters.TEXT & ~filters.COMMAND, add_product_description)
            ],
            ADD_PRODUCT_SITUATION: [
                MessageHandler(filters.Regex("^اضافه کردن محصول$"), add_product_button),
                MessageHandler(filters.Regex("^لغو عملیات!$"), admin_owner_panel_break_conversation),
                MessageHandler(filters.TEXT & ~filters.COMMAND, add_product_situation)
            ],
            ADD_PRODUCT_IMAGE_ID: [
                MessageHandler(filters.Regex("^اضافه کردن محصول$"), add_product_button),
                MessageHandler(filters.Regex("^لغو عملیات!$"), admin_owner_panel_break_conversation),
                CallbackQueryHandler(add_product_image_id, pattern=r"^(True|False) -ap$"),
            ],
            ADD_PRODUCT: [
                MessageHandler(filters.Regex("^اضافه کردن محصول$"), add_product_button),
                MessageHandler(filters.Regex("^لغو عملیات!$"), admin_owner_panel_break_conversation),
                MessageHandler(filters.PHOTO | filters.TEXT, add_product)
            ],
        },
        fallbacks=[CommandHandler('done', break_conversation)],
    )

    return add_product_conv_handler