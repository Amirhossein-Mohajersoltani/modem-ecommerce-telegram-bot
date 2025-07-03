from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, CallbackQuery
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CallbackQueryHandler, \
    CommandHandler
from bot.core.database import *
from bot.core.utils import *
import json

database = Database()


# States
MODEM_MODEL_OPTIONS_BUY, MODEM_NAME_OPTIONS_BUY, MODEM_DESCRIPTION_BUY, MODEM_COUNT_BUY, STORE_MODEM_BUY = range(5)






# Start Point
async def modem_situation_options_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not database.is_contain(update.effective_chat.id, "users", f"chat_id = {update.effective_chat.id}"):
        return ConversationHandler.END

    context.user_data.clear()
    context.user_data["modem_conv"] = True



    # check for modem situation availability
    modem_situation_availability = {}
    modems = database.fetch_data("modem")
    for modem in modems:
        if modem[5] > 0 and modem[3] == 0 and "pre-owned" not in modem_situation_availability:
            modem_situation_availability["pre-owned"] = True
        elif modem[5] > 0 and modem[3] == 1 and "newbie" not in modem_situation_availability:
            modem_situation_availability["newbie"] = True

    # Both
    if modem_situation_availability.get("pre-owned") and modem_situation_availability.get("newbie"):
        # preparing message
        text = get_dynamic_text("modem","modem_situation_options_buy", "message")
        keyboard = [
            [
                InlineKeyboardButton(
                    get_dynamic_text("modem","modem_situation_options_buy", "option_new"),
                    callback_data="newbie"
                ),
                InlineKeyboardButton(
                    get_dynamic_text("modem","modem_situation_options_buy","option_pre-owned"),
                    callback_data="pre-owned"
                ),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)



        await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
        return MODEM_MODEL_OPTIONS_BUY

    # Newbie
    elif modem_situation_availability.get("newbie"):
        context.user_data["modem_situation"] = "newbie"
        return await modem_model_options_buy(update, context)

    # Pre-owned
    elif modem_situation_availability.get("pre-owned"):
        context.user_data["modem_situation"] = "pre-owned"
        return await modem_model_options_buy(update, context)

    # neither
    else:
        # No Inventory Text
        text = get_dynamic_text("modem","modem_situation_options_buy","no_inventory")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return ConversationHandler.END





# CHOOSE_MODEM_MODEL
async def modem_model_options_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # singular conv checker
    if context.user_data.get('update_user_info_conv') or context.user_data.get('payment_conv') or context.user_data.get('simcard_conv'):
        return ConversationHandler.END

    if update.callback_query:
        # getting callback query and send response
        query = update.callback_query
        await query.answer()

        # Save Situation
        if query.data == "newbie":
            context.user_data["is_new"] = True
        elif query.data == "pre-owned":
            context.user_data["is_new"] = False
    # In Case which the function Directly Called via previous step
    else:
        if context.user_data["modem_situation"] == "newbie":
            context.user_data["is_new"] = True
        elif context.user_data["modem_situation"] == "pre-owned":
            context.user_data["is_new"] = False

    # To prevent continuing steps if the required data does not exist with any reason
    if context.user_data.get("is_new") is None:
        return ConversationHandler.END


    # Get Text From Dynamic Text File
    text = get_dynamic_text("modem","modem_model_options_buy","message")



    # Dynamically show users the available modems
    modem_availability = []
    keyboard = []
    result = database.fetch_data("modem")

    for modem in result:
        if modem[5] > 0 and modem[3] == context.user_data["is_new"] and modem[1] not in modem_availability:
            model = modem[1]
            # Dynamic the text
            additional_data = {"{model}": model}
            modem_availability.append(model)
            inline_keyboard = [
                InlineKeyboardButton(
                    get_dynamic_text("modem", "modem_model_options_buy", "model_options", additional_data=additional_data),
                    callback_data=f"{model} -m")
            ]
            keyboard.append(inline_keyboard)

    # To check this function doesn't called directly
    if not context.user_data.get("modem_situation"):
        keyboard.append(
            [
                InlineKeyboardButton(
                    get_dynamic_text("modem", "modem_model_options_buy", "return_option"),
                    callback_data="return_modem_situation_options_buy"
                )
            ]
        )
    reply_markup = InlineKeyboardMarkup(keyboard)

    if context.user_data.get("modem_situation"):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
    else:
        await query.edit_message_text(text=text,reply_markup=reply_markup)

    return MODEM_NAME_OPTIONS_BUY



# MODEM_NAME_OPTIONS_BUY
# ---------------------------------------------------
# Check Here
async def modem_name_options_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # singular conv checker
    if context.user_data.get('update_user_info_conv') or context.user_data.get('payment_conv') or context.user_data.get('simcard_conv'):
        return ConversationHandler.END


    # getting callback query and send response
    query = update.callback_query
    await query.answer()

    # Handle model models and return button
    if query.data == "5G -m" or query.data == "TD-LTE -m" or query.data == "4G -m":
        context.user_data["model"] = query.data.split()[0]
    elif query.data == "return_modem_situation_options_buy":
        return await modem_situation_options_buy(update, context)


    # Check all the requirements data to be available
    if not context.user_data.get("model") or context.user_data.get("is_new") is None:
        return ConversationHandler.END


    # Fetch all the data with chosen option model and situation
    modems = database.fetch_data("modem",f"model = '{context.user_data["model"]}' and is_new = {context.user_data['is_new']}")
    text = get_dynamic_text("modem","modem_name_options_buy","message")
    # save name, id and price of available modems for later
    modems_data = [{"name":modem[2],"id":modem[0]} for modem in modems if int(modem[5]) > 0]


    # create dynamic keyboard for each product with condition "count > 0" from the previous line of code
    keyboard = [
        [
            InlineKeyboardButton(
            get_dynamic_text("modem", "modem_name_options_buy", "name_options", additional_data={"{modem_name}":modem_data["name"]}),
            callback_data=f"{modem_data["id"]} -m"
            )
        ] for modem_data in modems_data
    ]
    keyboard.append(
        [
            InlineKeyboardButton(
                text=get_dynamic_text("modem", "modem_name_options_buy", "return_option"),
                callback_data="return_modem_model_options_buy"
            )
        ]
    )
    reply_markup = InlineKeyboardMarkup(keyboard)


    # Handle the return situation and update response
    if context.user_data.get("return_modem_name_options_buy"):
        # set to default to change everything back
        context.user_data["return_modem_name_options_buy"] = False

        # to edit the message had been sent that has a picture
        await query.delete_message()
        await query.message.chat.send_message(
            text=text,
            reply_markup=reply_markup
        )
    else:
        # when that message doesn't have picture
        await query.edit_message_text(text=text,reply_markup=reply_markup)


    return MODEM_DESCRIPTION_BUY




# CHOOSE_SHOW_DESCRIPTION
async def modem_description_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # singular conv checker
    if context.user_data.get('update_user_info_conv') or context.user_data.get('payment_conv') or context.user_data.get('simcard_conv'):
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()

    # Handle the return Keyboard and others
    if query.data == "return_modem_model_options_buy":
        return await modem_model_options_buy(update, context)
    else:
        # modem data has been sent via callback query with type string
        context.user_data["product_id"] = query.data.split()[0]


    # to check that all the previous states had been passed, and we are not outside the conv
    if not context.user_data.get("product_id"):
        return ConversationHandler.END

    # fetch data about selected modem (Description and File ID)
    selected_modem = database.fetch_data("modem",f"id = '{context.user_data["product_id"]}'")

    description = selected_modem[0][7]
    file_id = selected_modem[0][6]
    name = selected_modem[0][2]
    model = selected_modem[0][1]
    price = selected_modem[0][4]
    inventory = selected_modem[0][5]
    if selected_modem[0][3]:
        situation = "آکبند"
    else:
        situation = "استوک"

    additional_data = {
        "{description}": description,
        "{name}": name,
        "{model}": model,
        "{price}": price,
        "{inventory}": inventory,
        "{situation}": situation
    }

    text = get_dynamic_text("modem", "modem_description_buy","message", additional_data=additional_data)


    # Create keyboards
    keyboard = [
        [
            InlineKeyboardButton(
                text=get_dynamic_text("modem", "modem_description_buy", "buy_option", additional_data=additional_data),
                callback_data="buy -m")
        ],
        [
            InlineKeyboardButton(
                text=get_dynamic_text("modem", "modem_description_buy", "return_option"),
                callback_data="return_modem_name_options_buy")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Handle sending message with or without picture
    if file_id != "0":
        await query.edit_message_media(
            media=InputMediaPhoto(
                media=file_id,
                caption=text
            ),
            reply_markup=reply_markup
        )
    else:
        await query.edit_message_text(text=text,reply_markup=reply_markup)


    return MODEM_COUNT_BUY


# MODEM_COUNT_BUY
async def modem_count_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # singular conv checker
    if context.user_data.get('update_user_info_conv') or context.user_data.get('payment_conv') or context.user_data.get('simcard_conv'):
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()

    # Handle the user decision
    if query.data == "return_modem_name_options_buy":
        context.user_data["return_modem_name_options_buy"] = True
        return await modem_name_options_buy(update, context)
    elif query.data == "buy -m":
        reply_markup = create_user_break_button()
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=get_dynamic_text("modem","modem_count_buy", "message"),
            reply_markup=reply_markup
        )

        return STORE_MODEM_BUY



# MODEM_COUNT_BUY
async def store_modem_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # singular conv checker
    if context.user_data.get('update_user_info_conv') or context.user_data.get('payment_conv') or context.user_data.get('simcard_conv'):
        return ConversationHandler.END

    # Check for flow correctness
    if not context.user_data.get("product_id"):
        return ConversationHandler.END

    # Determine the order count
    user_input = convert_numbers(update.message.text).strip()

    product = database.fetch_data("modem",f"id = '{context.user_data['product_id']}'")
    inventory = product[0][5]
    name = product[0][2]
    additional_data = {
        "{name}": name,
        "{inventory}": inventory,
        "{user_input}": user_input
    }

    if not is_valid_number(user_input):
        await update.message.reply_text(get_dynamic_text("modem", "store_modem_buy","invalid_number"))
        return STORE_MODEM_BUY
    elif int(user_input) > inventory:
        await update.message.reply_text(get_dynamic_text("modem", "store_modem_buy","no_inventory", additional_data=additional_data))
        return STORE_MODEM_BUY


    # Store Data: product_id in available in context.user_data
    context.user_data["product_table"] = "modem"
    context.user_data['product_count'] = int(user_input)
    # Save the Chat id
    context.user_data["chat_id"] = update.effective_chat.id


    record = Record(
        table_name="cart_items",
        product_table= context.user_data["product_table"],
        product_id=context.user_data["product_id"],
        product_count=context.user_data["product_count"],
        chat_id=context.user_data["chat_id"]
    )
    database.add_record(record)


    text = get_dynamic_text("modem","store_modem_buy","message")
    reply_markup = create_user_panel()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
    return ConversationHandler.END



# Handler
def modem_handler():
    modem_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^خرید مودم$"), modem_situation_options_buy)],
        states={
            MODEM_MODEL_OPTIONS_BUY: [
                MessageHandler(filters.Regex("^خرید مودم$"), modem_situation_options_buy),
                CallbackQueryHandler(modem_model_options_buy, pattern="^pre-owned|newbie$"),
            ],
            MODEM_NAME_OPTIONS_BUY: [
                MessageHandler(filters.Regex("^خرید مودم$"), modem_situation_options_buy),
                CallbackQueryHandler(modem_name_options_buy, pattern="^((5G|TD-LTE|4G) -m|return_modem_situation_options_buy)$"),
            ],
            MODEM_DESCRIPTION_BUY: [
                MessageHandler(filters.Regex("^خرید مودم$"), modem_situation_options_buy),
                CallbackQueryHandler(modem_description_buy, pattern=r"^\d+ -m$|return_modem_model_options_buy$")
            ],
            MODEM_COUNT_BUY: [
                MessageHandler(filters.Regex("^خرید مودم$"), modem_situation_options_buy),
                CallbackQueryHandler(modem_count_buy, pattern="^buy -m|return_modem_name_options_buy$")
            ],
            STORE_MODEM_BUY: [
                MessageHandler(filters.Regex("^خرید مودم$"), modem_situation_options_buy),
                MessageHandler(filters.Regex("^لغو عملیات!$"), user_panel_break_conversation),
                MessageHandler(filters.TEXT & (~filters.COMMAND), store_modem_buy),
            ]
        },
        fallbacks=[CommandHandler('done', user_panel_break_conversation)],
    )
    return modem_conv_handler