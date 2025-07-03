from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CallbackQueryHandler, \
    CommandHandler
from bot.core.database import *
from bot.core.utils import *


database = Database()


UPDATE_GET_PRODUCT_ID, UPDATE_SHOW_OPTIONS, UPDATE_CONVERSATION_CONTROL = range(3)


# Start Point
async def update_record_button(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # Check user is admin ot not
    if database.is_admin(update.effective_chat.id):
        context.user_data.clear()
        context.user_data["update_record"] = True


        keyboard = [
            [
                InlineKeyboardButton("مودم", callback_data="modem -up"),
                InlineKeyboardButton(text="سیمکارت", callback_data="simcard -up"),
            ],
            ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        text = "لطفا یکی از گزینه های زیر را انتخاب کنید:"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
        return UPDATE_GET_PRODUCT_ID
    return ConversationHandler.END

#     ----------------------------
async def update_get_product_id(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get(
        'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user') or context.user_data.get('add_owner'):
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()
    context.user_data["table_name"] = query.data.split()[0]
    context.user_data["model"] = None
    context.user_data["name"] = None
    context.user_data["price"] = None
    context.user_data["count"] = None
    context.user_data["description"] = None
    context.user_data["is_new"] = None
    context.user_data["image_id"] = None


    result = database.fetch_data(context.user_data["table_name"])
    if context.user_data["table_name"] == "modem":
        show_result = show_admin_modems(result)
    else:
        show_result = show_admin_simcards(result)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=show_result)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="لطفا آیدی محصول را وارد کنید.")
    context.user_data["set"] = "id"
    return UPDATE_SHOW_OPTIONS




async def update_show_options(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get(
        'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user') or context.user_data.get('add_owner'):
        return ConversationHandler.END

    # Get Different Types of Input
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        data = query.data
    elif update.message:
        message = update.message.text


    # Set ID
    if context.user_data["set"] == "id":
        user_input = convert_numbers(message).strip()
        # Check if ID is Valid or Not
        if not user_input.isdigit():
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="آیدی تنها شامل اعداد صحیح غیر صفر می باشد.\nلطفا دوباره آیدی را ارسال کنید:"
            )
            # Ask to enter again before continue
            return UPDATE_SHOW_OPTIONS

        admin_id = int(user_input)
        if not database.is_contain(admin_id, context.user_data["table_name"], f" id = {admin_id}"):
            text = "مقدار آیدی معتبر نمی باشد.\nلطفا دوباره آیدی را ارسال کنید:"

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
            )
            # Ask to enter again before continue
            return UPDATE_SHOW_OPTIONS

        # Valid IP
        context.user_data["id"] = message

    # Set Model
    elif context.user_data["set"] == "model":
        context.user_data["model"] = data.split()[0]

    # Set Name
    elif context.user_data["set"] == "name":
        context.user_data["name"] = message

    # Set Price
    elif context.user_data["set"] == "price":
        if not update.message.text.isdigit():
            text = "قیمت وارد شده معتبر نمی باشد\nلطفا مجددا قیمت محصول را وارد کنید:"
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
            return UPDATE_SHOW_OPTIONS
        context.user_data["price"] = message

    # Set Count
    elif context.user_data["set"] == "count":
        if not update.message.text.isdigit():
            text = "مقدار وارد شده صحیح نیست. تعداد محصول باید یک عدد صحیح مثبت باشد.\nلطفا مجدد تعداد را وارد کنید:"
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
            return UPDATE_SHOW_OPTIONS
        context.user_data["count"] = message

    # Set Description
    elif context.user_data["set"] == "description":
        context.user_data["description"] = message

    # Set Situation
    elif context.user_data["set"] == "is_new":
        if data.split()[0] == "1":
            context.user_data["is_new"] = True
        else:
            context.user_data["is_new"] = False

    # Set Image ID
    elif context.user_data["set"] == "image_id":
        # Check for input Validation and save image id
        if update.message.photo:
            file_id = update.message.photo[-1].file_id
            context.user_data["image_id"] = file_id
        elif update.message.text == "0":
            context.user_data["image_id"] = "0"
        else:
            text = "لطفا مقدار معتبر وارد کنید:"
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
            return UPDATE_SHOW_OPTIONS




    if context.user_data["table_name"] == "modem":
        keyboard_options = [
            [
                InlineKeyboardButton(text="(4G/5G/TD-LTE)مدل", callback_data="model -up"),
                InlineKeyboardButton(text="نام محصول", callback_data="name -up")
            ],
            [
                InlineKeyboardButton(text="توضیحات", callback_data="description -up"),
                InlineKeyboardButton(text="استوک/آکبند", callback_data="is_new -up")
            ],
            [
                InlineKeyboardButton(text="قیمت", callback_data="price -up"),
                InlineKeyboardButton(text="تعداد", callback_data="count -up")
            ],
            [
                InlineKeyboardButton(text="عکس", callback_data="image_id -up")
            ],
            [
                InlineKeyboardButton(text="اضافه", callback_data="add -up")
            ],
            [
                InlineKeyboardButton(text="لغو عملیات!", callback_data="cancel -up")
            ]
        ]
    else:
        keyboard_options = [
            [
                InlineKeyboardButton(text="(4G/5G/TD-LTE)مدل", callback_data="model -up"),
                InlineKeyboardButton(text="نام محصول", callback_data="name -up"),
            ],
            [
                InlineKeyboardButton(text="قیمت", callback_data="price -up"),
                InlineKeyboardButton(text="تعداد", callback_data="count -up"),
            ],
            [
                InlineKeyboardButton(text="توضیحات", callback_data="description -up")
            ],
            [
                InlineKeyboardButton(text="اضافه", callback_data="add -up")
            ],
            [
                InlineKeyboardButton(text="لغو عملیات!", callback_data="cancel -up")
            ]
        ]

    reply_markup = InlineKeyboardMarkup(keyboard_options)

    await context.bot.send_message(chat_id=update.effective_chat.id, text="لطفا یکی از موارد زیر را انتخاب کنید:",reply_markup=reply_markup)
    return UPDATE_CONVERSATION_CONTROL






async def update_model(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get(
        'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user') or context.user_data.get('add_owner'):
        return ConversationHandler.END



    keyboard = [
        [
            InlineKeyboardButton("5G", callback_data="5G -up"),
        ],
        [
            InlineKeyboardButton("TD-LTE", callback_data="TD-LTE -up"),
        ],
        [
            InlineKeyboardButton("4G", callback_data="4G -up"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "لطفا مدل محصول را انتخاب کنید:"
    await context.bot.send_message(chat_id=update.effective_chat.id,text=text, reply_markup=reply_markup)

    context.user_data["set"] = "model"

    return UPDATE_SHOW_OPTIONS




async def update_name(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get(
        'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user') or context.user_data.get('add_owner'):
        return ConversationHandler.END

    text = "لطفا یک نام برای محصول وارد کنید.\nاز این نام برای معرفی محصول به کاربر استفاده می شود."
    await context.bot.send_message(chat_id=update.effective_chat.id,text=text)

    context.user_data["set"] = "name"

    return UPDATE_SHOW_OPTIONS





async def update_price(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get(
        'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user') or context.user_data.get('add_owner'):
        return ConversationHandler.END


    text = "لطفا قیمت محصول را وارد کنید:"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    context.user_data["set"] = "price"

    return UPDATE_SHOW_OPTIONS




async def update_count(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get(
        'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user') or context.user_data.get('add_owner'):
        return ConversationHandler.END


    text = "لطفا میزان موجودی را وارد کنید:"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    context.user_data["set"] = "count"

    return UPDATE_SHOW_OPTIONS





async def update_description(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get(
        'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user') or context.user_data.get('add_owner'):
        return ConversationHandler.END

    text = "لطفا متن توضیحات محصول را وارد کنید.\nاز این متن برای نمایش به کاربر استفاده می شود."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    context.user_data["set"] = "description"

    return UPDATE_SHOW_OPTIONS



async def update_is_new(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get(
        'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user') or context.user_data.get('add_owner'):
        return ConversationHandler.END


    keyboard = [
        [
            InlineKeyboardButton("مودم آکبند", callback_data="1 -up"),
            InlineKeyboardButton("مودم استوک", callback_data="0 -up")
        ],
    ]
    text = "لطفا گزینه مناسب را انتخاب کنید:"
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)

    context.user_data["set"] = "is_new"

    return UPDATE_SHOW_OPTIONS




async def update_image_id(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get(
        'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user') or context.user_data.get('add_owner'):
        return ConversationHandler.END

    text = "لطفا درصورت وجود، عکس محصول را ارسال کنید در غیر این صورت 0 وارد کنید:"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=None)

    context.user_data["set"] = "image_id"

    return UPDATE_SHOW_OPTIONS




async def update_product(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get(
        'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user') or context.user_data.get('add_owner'):
        return ConversationHandler.END

    if database.update_record(Record(
        table_name=context.user_data["table_name"],
        product_model= context.user_data["model"],
        product_description=context.user_data["description"],
        product_price=context.user_data["price"],
        product_count=context.user_data["count"],
        product_name=context.user_data["name"],
        file_id=context.user_data["image_id"],
        is_new=context.user_data["is_new"]
        ),
        f"id = {context.user_data['id']}"
    ):
        text= "عملیات با موفقیت انجام شد."
    else:
        text = "مشکلی در اضافه کردن رکورد به وجود آمده است!"

    reply_markup = create_admin_panel()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
    context.user_data.clear()
    return ConversationHandler.END

# Handler
def update_record_handler():
    update_product_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^ویرایش محصول$"), update_record_button)],
        states={
            UPDATE_GET_PRODUCT_ID: [
                MessageHandler(filters.Regex("^ویرایش محصول$"), update_record_button),
                MessageHandler(filters.Regex("^لغو عملیات!$"), admin_owner_panel_break_conversation),
                CallbackQueryHandler(update_get_product_id, pattern=r"^(modem|simcard) -up$"),
            ],
            UPDATE_SHOW_OPTIONS: [
                MessageHandler(filters.Regex("^ویرایش محصول$"), update_record_button),
                MessageHandler(filters.Regex("^لغو عملیات!$"), admin_owner_panel_break_conversation),
                MessageHandler(filters.PHOTO | filters.TEXT & ~filters.COMMAND, update_show_options),
                CallbackQueryHandler(update_show_options, pattern=r"^(1|0|4G|TD-LTE|5G) -up$")
            ],
            UPDATE_CONVERSATION_CONTROL: [
                MessageHandler(filters.Regex("^ویرایش محصول$"), update_record_button),
                MessageHandler(filters.Regex("^لغو عملیات!$"), admin_owner_panel_break_conversation),
                CallbackQueryHandler(admin_owner_panel_break_conversation, pattern=r"^cancel -up$"),
                CallbackQueryHandler(update_model, pattern=r"^model -up$"),
                CallbackQueryHandler(update_name, pattern=r"^name -up$"),
                CallbackQueryHandler(update_price, pattern=r"^price -up$"),
                CallbackQueryHandler(update_count, pattern=r"^count -up$"),
                CallbackQueryHandler(update_description, pattern=r"^description -up$"),
                CallbackQueryHandler(update_is_new, pattern=r"^is_new -up$"),
                CallbackQueryHandler(update_image_id, pattern=r"^image_id -up$"),
                CallbackQueryHandler(update_product, pattern=r"^add -up$")
            ],
        },
        fallbacks=[CommandHandler('done', break_conversation)],
    )
    return update_product_conv_handler