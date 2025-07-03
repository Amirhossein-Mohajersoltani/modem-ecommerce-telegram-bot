from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CallbackQueryHandler, \
    CommandHandler
from database import *
from utils import *


database = Database()

# States
SHOW_PRODUCTS_MODEL, SHOW_MODEM_MODEL, SHOW_MODEM_NAMES, SHOW_SIMCARD_NAMES, SHOW_MODEM_INFORMATION, SHOW_SIMCARD_INFORMATION ,SHOW_FINISHED = range(7)


# Start Point
async def show_products_table(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(database.is_owner(update.effective_chat.id))
    if database.is_admin(update.effective_chat.id) or database.is_owner(update.effective_chat.id):
        context.user_data.clear()
        context.user_data["show_product"] = True


        keyboard = [
            [
                InlineKeyboardButton("مودم", callback_data="modem -sp"),
                InlineKeyboardButton("سیمکارت", callback_data="simcard -sp")
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = "لطفا گزینه دلخواه خود را انتخاب کنید:"

        if context.user_data.get("return-show-products-table"):
            context.user_data["return-show-products-table"] = False
            query = update.callback_query
            await query.edit_message_text(text=text, reply_markup=reply_markup)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)


        return SHOW_PRODUCTS_MODEL
    return ConversationHandler.END



# SHOW_PRODUCTS_MODEL
async def show_product_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if (context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or
            context.user_data.get("update_record") or context.user_data.get(
        'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user') or context.user_data.get('add_owner')):
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()

    if query.data == "modem -sp" or query.data == "simcard -sp":
        context.user_data['table'] = query.data.split()[0]

    text = "لطفا یکی از گزینه های زیر را انتخاب کنید."

    if context.user_data['table'] == "modem":

        keyboard = [
            [
                InlineKeyboardButton("مودم آکبند", callback_data="new -sp"),
            ],
            [
                InlineKeyboardButton("مودم استوک", callback_data="pre-owned -sp"),
            ],
            [
                InlineKeyboardButton("بازگشت", callback_data="return-show-products-table"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)


        await query.edit_message_text(text=text, reply_markup=reply_markup)
        return SHOW_MODEM_MODEL

    else:
        keyboard = [
            [
                InlineKeyboardButton("سیمکارت 5G", callback_data="5G -sp")
            ],
            [
                InlineKeyboardButton("سیمکارت TD-LTE", callback_data="TD-LTE -sp")
            ],
            [
                InlineKeyboardButton("سیمکارت 4G", callback_data="4G -sp")
            ],
            [
                InlineKeyboardButton("بازگشت", callback_data="return-show-products-table"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)



        await query.edit_message_text(text=text, reply_markup=reply_markup)


        return SHOW_SIMCARD_NAMES







# SHOW_MODEM_MODEL
async def show_modem_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if (context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or
            context.user_data.get("update_record") or context.user_data.get(
                'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
                'delete_user') or context.user_data.get('add_owner')):
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()

    # Save Situation
    if query.data == "return-show-products-table":
        context.user_data["return-show-products-table"] = True
        return await show_products_table(update, context)
    elif query.data == "new -sp":
        context.user_data["is_new"] = True
    elif query.data == "pre-owned -sp":
        context.user_data["is_new"] = False

    text = "لطفا یکی از گزینه های زیر را انتخاب کنید."

    keyboard = [
        [
            InlineKeyboardButton("مودم 5G", callback_data="5G -sp")
        ],
        [
            InlineKeyboardButton("مودم TD-LTE", callback_data="TD-LTE -sp")
        ],
        [
            InlineKeyboardButton("مودم 4G", callback_data="4G -sp")
        ],
        [
            InlineKeyboardButton("بازگشت", callback_data="return-show-product-model")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(reply_markup=reply_markup,text=text)

    return SHOW_MODEM_NAMES



# SHOW_MODEM_NAMES
async def show_modem_names(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if (context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or
            context.user_data.get("update_record") or context.user_data.get(
                'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
                'delete_user') or context.user_data.get('add_owner')):
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()

    # Handle model names and return button
    if query.data == "5G -sp" or query.data == "TD-LTE -sp" or query.data == "4G -sp":
        context.user_data["model"] = query.data.split()[0]
    elif query.data == "return-show-product-model":
        return await show_product_model(update, context)

    # Fetch all the data with chosen option model and situation
    modems = database.fetch_data("modem",f"model = '{context.user_data['model']}' and is_new = {context.user_data['is_new']}")



    # Check whether the result is empty or not
    if not modems:
        text = "مودمی یافت نشد!"
        await query.edit_message_text(text=text)
        return ConversationHandler.END


    text = "لطفا مودم دلخواه خودتان را انتخاب کنید."
    # save name, id and price for later
    modems_data = [{"name":modem[2],"id":modem[0]} for modem in modems]


    # create keyboard for each product
    keyboard = [[InlineKeyboardButton(modem_data["name"], callback_data=f"{modem_data["id"]} -sp")] for modem_data in modems_data]
    keyboard.append([InlineKeyboardButton(text="بازگشت", callback_data="return-show-modem-model")])
    reply_markup = InlineKeyboardMarkup(keyboard)


    # Handle the return situation and update response
    if context.user_data.get("is-contain-picture"):
        context.user_data["is-contain-picture"] = False
        # for edit the message has been sent has a picture
        await query.delete_message()
        await query.message.chat.send_message(
            text=text,
            reply_markup=reply_markup
        )
    else:
        # when that message doesn't have picture
        await query.edit_message_text(text=text,reply_markup=reply_markup)


    return SHOW_MODEM_INFORMATION




# SHOW_SIMCARD_NAMES
async def show_simcard_names(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if (context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or
            context.user_data.get("update_record") or context.user_data.get(
                'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
                'delete_user') or context.user_data.get('add_owner')):
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()

    # Save Simcard Model
    if query.data == "return-show-products-table":
        return await show_products_table(update, context)
    elif query.data == "5G -sp" or query.data == "TD-LTE -sp" or query.data == "4G -sp":
        context.user_data["model"] = query.data.split()[0]



    # fetch simcards data where "model = <Chosen_Model>"
    simcards = database.fetch_data("simcard", f"model = '{context.user_data["model"]}'")
    # Check whether the result is empty or not
    if not simcards:
        text = "سیمکارتی یافت نشد!"
        await query.edit_message_text(text=text)
        return ConversationHandler.END

    # create dict for each product with name , id , price
    simcards_data = [{"name":simcard[2],"id":simcard[0]} for simcard in simcards]
    # Create keyboards where "count>0" from previous line of code
    keyboard = [[InlineKeyboardButton(simcard_data["name"], callback_data=f"{simcard_data["id"]} -sp")] for simcard_data in simcards_data]
    # Create Back Button
    keyboard.append([InlineKeyboardButton(text="بازگشت", callback_data="return-show-product-model")])
    reply_markup = InlineKeyboardMarkup(keyboard)


    text = "لطفا سیمکارت مورد نظر را انتخاب کنید."
    await query.edit_message_text(text=text,reply_markup=reply_markup)
    return SHOW_SIMCARD_INFORMATION




# SHOW_MODEM_INFORMATION
async def show_modem_information(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if (context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or
            context.user_data.get("update_record") or context.user_data.get(
                'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
                'delete_user') or context.user_data.get('add_owner')):
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()

    # Handle the return Keyboard and others
    if query.data == "return-show-modem-model":
        return await show_modem_model(update, context)
    else:
        # modem data has been sent via callback query with type string
        context.user_data["id"] = query.data.split()[0]



    # fetch data about selected modem (Description and File ID)
    selected_modem = database.fetch_data("modem",f"id = {context.user_data['id']}")

    description = selected_modem[0][7]
    file_id = selected_modem[0][6]

    text = show_admin_modems(selected_modem)

    # Create keyboards
    keyboard = [
        [
            InlineKeyboardButton(text="اتمام!",callback_data="finish -sp")
        ],
        [
            InlineKeyboardButton(text="بازگشت",callback_data="return-show-modem-names")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Handle sending message with or without picture
    if file_id != "0":
        try:
            context.user_data["is-contain-picture"] = True
            await query.edit_message_media(
                media=InputMediaPhoto(
                    media=file_id,
                    caption=text
                ),
                reply_markup=reply_markup
            )
        except Exception as e:
            context.user_data["is-contain-picture"] = False
            await query.edit_message_text(text=text, reply_markup=reply_markup)

    else:
        context.user_data["is-contain-picture"] = False
        await query.edit_message_text(text=text,reply_markup=reply_markup)


    return SHOW_FINISHED



# SHOW_SIMCARD_INFORMATION
async def show_simcard_information(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if (context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or
            context.user_data.get("update_record") or context.user_data.get(
                'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
                'delete_user') or context.user_data.get('add_owner')):
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()



    # Callback Handler
    if query.data == "return-show-product-model":
        return await show_product_model(update, context)
    else:
        context.user_data["id"] = query.data.split()[0]



    # Fetch Description to Show Users
    selected_simcard = database.fetch_data("simcard",f"id = {context.user_data['id']}")


    text = show_admin_simcards(selected_simcard)

    keyboard = [
        [
            InlineKeyboardButton(text="اتمام!",callback_data="finish -sp")
        ],
        [
            InlineKeyboardButton(text="بازگشت",callback_data="return-show-simcard-names")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)


    await query.edit_message_text(text=text,reply_markup=reply_markup)
    return SHOW_FINISHED



# SHOW_FINISHED
async def show_finished(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if (context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or
            context.user_data.get("update_record") or context.user_data.get(
                'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
                'delete_user') or context.user_data.get('add_owner')):
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()

    # Handle the user decision
    if query.data == "return-show-modem-names":
        return await show_modem_names(update, context)
    elif query.data == "return-show-simcard-names":
        return await show_simcard_names(update, context)
    elif query.data == "finish -sp":
        return ConversationHandler.END



# SHOW_PRODUCTS_MODEL, SHOW_MODEM_MODEL, SHOW_MODEM_NAMES, SHOW_SIMCARD_NAMES, SHOW_MODEM_INFORMATION, SHOW_SIMCARD_INFORMATION ,SHOW_FINISHED
# Handler
def show_product_handler():
    show_product_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^نمایش محصولات$"), show_products_table)],
        states={
            SHOW_PRODUCTS_MODEL: [
                MessageHandler(filters.Regex("^نمایش محصولات$"), show_products_table),
                CallbackQueryHandler(show_product_model, pattern=r"^(modem|simcard) -sp$"),
            ],
            SHOW_MODEM_MODEL: [
                MessageHandler(filters.Regex("^نمایش محصولات$"), show_products_table),
                CallbackQueryHandler(show_modem_model, pattern=r"^(4G|TD-LTE|5G|new|pre-owned) -sp|return-show-products-table$"),
            ],
            SHOW_MODEM_NAMES: [
                MessageHandler(filters.Regex("^نمایش محصولات$"), show_products_table),
                CallbackQueryHandler(show_modem_names, pattern=r"^(4G|TD-LTE|5G) -sp|return-show-product-model$"),
            ],
            SHOW_SIMCARD_NAMES: [
                MessageHandler(filters.Regex("^نمایش محصولات$"), show_products_table),
                CallbackQueryHandler(show_simcard_names, pattern=r"^(4G|TD-LTE|5G) -sp|return-show-products-table$"),
            ],
            SHOW_MODEM_INFORMATION: [
                MessageHandler(filters.Regex("^نمایش محصولات$"), show_products_table),
                CallbackQueryHandler(show_modem_information, pattern=r"^\d+ -sp$|return-show-modem-model$"),
            ],
            SHOW_SIMCARD_INFORMATION: [
                MessageHandler(filters.Regex("^نمایش محصولات$"), show_products_table),
                CallbackQueryHandler(show_simcard_information, pattern=r"^\d+ -sp$|return-show-product-model$"),
            ],
            SHOW_FINISHED: [
                MessageHandler(filters.Regex("^نمایش محصولات$"), show_products_table),
                CallbackQueryHandler(show_finished, pattern=r"^finish -sp|return-show-modem-names|return-show-simcard-names$"),
            ]
        },
        fallbacks=[CommandHandler('done', admin_owner_panel_break_conversation)],
    )
    return show_product_conv_handler




