from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CallbackQueryHandler, \
    CommandHandler
from bot.core.database import *
from bot.core.utils import *


database = Database()


# States
SIMCARD_NAME_OPTIONS_BUY, SIMCARD_DESCRIPTION_BUY, SIMCARD_COUNT_BUY, STORE_SIMCARD_BUY = range(4)


# Start Point
async def simcard_model_options_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not database.is_contain(update.effective_chat.id, "users", f"chat_id = {update.effective_chat.id}"):
        return ConversationHandler.END

    context.user_data.clear()
    context.user_data['simcard_conv'] = True



    # Create Text and Keyboards
    text = get_dynamic_text("simcard", "simcard_model_options_buy", "message")

    # Dynamically show users the available simcard models
    result = database.fetch_data("simcard")
    simcard_availability = []
    keyboard = []
    for simcard in result:
        if simcard[4] > 0  and simcard[1] not in simcard_availability:
            model = simcard[1]
            additional_data = {
                "{model}": model
            }
            simcard_availability.append(model)
            inline_keyboard = [
                InlineKeyboardButton(
                    get_dynamic_text("simcard", "simcard_model_options_buy", "model_options", additional_data=additional_data),
                    callback_data=f"{model} -s"
                )
            ]
            keyboard.append(inline_keyboard)
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Check for the return button
    if context.user_data.get("return_simcard_model_options_buy"):
        context.user_data["return_simcard_model_options_buy"] = False
        await context.bot.edit_message_text(text=text, reply_markup=reply_markup)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id ,text=text,reply_markup=reply_markup)

    return SIMCARD_NAME_OPTIONS_BUY











# SIMCARD_NAME_OPTIONS_BUY
async def simcard_name_options_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # singular conv checker
    if context.user_data.get('update_user_info_conv') or context.user_data.get('payment_conv') or context.user_data.get('modem_conv'):
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()

    # Save Simcard Model
    if query.data == "5G -s" or query.data == "TD-LTE -s" or query.data == "4G -s":
        context.user_data["model"] = query.data.split()[0]

    # data flow checker
    if not context.user_data.get("model"):
        return ConversationHandler.END



    # fetch simcards data where "model = <Chosen_Model>"
    simcards = database.fetch_data("simcard", f"model = '{context.user_data.get("model")}'")
    # create dict for each product with name , id , price
    simcards_data = [{"name":simcard[2],"id":simcard[0]} for simcard in simcards if int(simcard[4]) > 0]
    # Create keyboards where "count>0" from previous line of code
    keyboard = [
        [
            InlineKeyboardButton(
                get_dynamic_text("simcard", "simcard_name_options_buy", "name_options", additional_data={"{simcard_name}": simcard_data["name"]}),
                callback_data=f"{simcard_data['id']} -s")
        ] for simcard_data in simcards_data
    ]
    # Create Back Button
    keyboard.append([InlineKeyboardButton(text="بازگشت", callback_data="return_simcard_model_options_buy")])
    reply_markup = InlineKeyboardMarkup(keyboard)


    text = get_dynamic_text("simcard", "simcard_name_options_buy", "message")
    await query.edit_message_text(text=text,reply_markup=reply_markup)
    return SIMCARD_DESCRIPTION_BUY







# SIMCARD_DESCRIPTION_BUY
async def simcard_description_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # singular conv checker
    if context.user_data.get('update_user_info_conv') or context.user_data.get('payment_conv') or context.user_data.get('modem_conv'):
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()



    # Callback Handler
    if query.data == "return_simcard_model_options_buy":
        context.user_data["return_simcard_model_options_buy"] = True
        return await simcard_model_options_buy(update, context)
    else:
        context.user_data["product_id"] = query.data.split()[0]


    if not context.user_data.get("product_id"):
        return ConversationHandler.END

    # Fetch Description to Show Users
    selected_simcard = database.fetch_data("simcard",f"id = '{context.user_data["product_id"]}'")
    description = selected_simcard[0][3]
    name = selected_simcard[0][2]
    model = selected_simcard[0][1]
    price = selected_simcard[0][5]
    inventory = selected_simcard[0][4]

    context.user_data["product_inventory"] = inventory
    context.user_data["product_name"] = name

    additional_data = {
        "{description}": description,
        "{name}": name,
        "{model}": model,
        "{price}": price,
        "{inventory}": inventory,
    }

    keyboard = [
        [
            InlineKeyboardButton(text=get_dynamic_text("simcard","simcard_description_buy","buy_option", additional_data=additional_data),callback_data="buy -s")
        ],
        [
            InlineKeyboardButton(text=get_dynamic_text("simcard","simcard_description_buy","return_option"),callback_data="return_simcard_name_options_buy")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)



    text = get_dynamic_text("simcard", "simcard_description_buy", "message", additional_data=additional_data)
    await query.edit_message_text(text=text,reply_markup=reply_markup)
    return SIMCARD_COUNT_BUY




# SIMCARD_COUNT_BUY
async def simcard_count_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # singular conv checker
    if context.user_data.get('update_user_info_conv') or context.user_data.get('payment_conv') or context.user_data.get('modem_conv'):
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()

    if not context.user_data.get("product_id"):
        return ConversationHandler.END

    if query.data == "return_simcard_name_options_buy":
        return await simcard_name_options_buy(update, context)

    reply_markup = create_user_break_button()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=get_dynamic_text("simcard","simcard_count_buy", "message"),
        reply_markup=reply_markup
    )

    return STORE_SIMCARD_BUY







# STORE_SIMCARD_BUY
async def store_simcard_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # singular conv checker
    if context.user_data.get('update_user_info_conv') or context.user_data.get('payment_conv') or context.user_data.get('modem_conv'):
        return ConversationHandler.END

    # Check for flow correctness
    if not context.user_data.get("product_id"):
        return ConversationHandler.END

    # Determine the order count
    user_input = convert_numbers(update.message.text).strip()

    additional_data = {
        "{name}": context.user_data["product_name"],
        "{inventory}": context.user_data["product_inventory"],
        "{user_input}": user_input
    }

    if not is_valid_number(user_input):
        await update.message.reply_text(get_dynamic_text("simcard", "store_simcard_buy", "invalid_number"))
        return STORE_SIMCARD_BUY
    elif int(user_input) > int(context.user_data["product_inventory"]):
        await update.message.reply_text(
            get_dynamic_text("simcard", "store_simcard_buy", "no_inventory", additional_data=additional_data),
        )
        return STORE_SIMCARD_BUY

    # Store Data: product_id in available in context.user_data
    context.user_data["product_table"] = "simcard"
    context.user_data['product_count'] = int(user_input)
    # Save the Chat id
    context.user_data["chat_id"] = update.effective_chat.id

    record = Record(
        table_name="cart_items",
        product_table=context.user_data["product_table"],
        product_id=context.user_data["product_id"],
        product_count=context.user_data["product_count"],
        chat_id=context.user_data["chat_id"]
    )
    database.add_record(record)


    text = get_dynamic_text("simcard", "store_simcard_buy", "message")
    reply_markup = create_user_panel()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
    return ConversationHandler.END





# Handler
def simcard_handler():

    simcard_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^خرید سیمکارت$"), simcard_model_options_buy)],
        states={
            SIMCARD_NAME_OPTIONS_BUY: [
                MessageHandler(filters.Regex("^خرید سیمکارت$"), simcard_model_options_buy),
                CallbackQueryHandler(simcard_name_options_buy, pattern="^(5G|TD-LTE|4G) -s$"),
            ],
            SIMCARD_DESCRIPTION_BUY: [
                MessageHandler(filters.Regex("^خرید سیمکارت$"), simcard_model_options_buy),
                CallbackQueryHandler(simcard_description_buy, pattern=r"^\d+ -s|return_simcard_model_options_buy$"),
            ],
            SIMCARD_COUNT_BUY: [
                MessageHandler(filters.Regex("^خرید سیمکارت$"), simcard_model_options_buy),
                CallbackQueryHandler(simcard_count_buy, pattern="^buy -s|return_simcard_name_options_buy$"),
            ],
            STORE_SIMCARD_BUY: [
                MessageHandler(filters.Regex("^خرید سیمکارت$"), simcard_model_options_buy),
                MessageHandler(filters.Regex("^لغو عملیات!$"), user_panel_break_conversation),
                MessageHandler(filters.TEXT & (~filters.COMMAND), store_simcard_buy),
            ]
        },

        fallbacks=[CommandHandler('done', user_panel_break_conversation)],
    )
    return simcard_conv_handler