from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telegram.ext import ConversationHandler, ContextTypes, MessageHandler, filters, CommandHandler, \
    CallbackQueryHandler
from database import *
from utils import *
import json



database = Database()

# States
SHOW_AVAILABLE_LEVELS_DYNAMIC, SHOW_AVAILABLE_PARTS_DYNAMIC, GET_NEW_TEXT_DYNAMIC, EDIT_TEXT_DYNAMIC  = range(4)



# Start Point
async def dynamic_text_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if database.is_admin(update.effective_chat.id) or database.is_owner(update.effective_chat.id):
        context.user_data.clear()
        context.user_data["dynamic_text"] = True

        with open("./dynamic_text.json", "r", encoding="utf-8") as t_file:
            content = json.load(t_file)

        keyboard = [
             [
                InlineKeyboardButton(key, callback_data=f"{key} -dt")
             ] for key,value in content.items()
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = "لطفا مکالمه مدنظر خود را انتخاب کنید:"

        await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
        return SHOW_AVAILABLE_LEVELS_DYNAMIC
    return ConversationHandler.END




# SHOW_AVAILABLE_LEVELS_DYNAMIC
async def show_available_conv_levels_dynamic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get("update_record") or context.user_data.get(
        'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user') or context.user_data.get('add_owner'):
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()

    query_data = query.data.split()[0]

    if query_data == "return_show_available_conv_levels_dynamic":
        pass
    else:
        context.user_data["conv_key"] = query_data


    with open("./dynamic_text.json", "r", encoding="utf-8") as t_file:
        content = json.load(t_file)

    keyboard = [
        [
            InlineKeyboardButton(key, callback_data=f"{key} -dt")
        ] for key, value in content[context.user_data["conv_key"]].items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "لطفا مرحله مدنظر خود را انتخاب کنید:"

    await query.edit_message_text(text=text, reply_markup=reply_markup)
    return SHOW_AVAILABLE_PARTS_DYNAMIC


# SHOW_AVAILABLE_PARTS_DYNAMIC
async def show_available_parts_dynamic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get("update_record") or context.user_data.get(
        'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user') or context.user_data.get('add_owner'):
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()

    query_data = query.data.split()[0]

    if query_data == "return_show_available_parts_dynamic":
        pass
    else:
        context.user_data["level_key"] = query_data


    with open("./dynamic_text.json", "r", encoding="utf-8") as t_file:
        content = json.load(t_file)

    keyboard = [
        [
            InlineKeyboardButton(key, callback_data=f"{key} -dt")
        ] for key, value in content[context.user_data["conv_key"]][context.user_data["level_key"]].items()
    ]
    keyboard.append(
        [
            InlineKeyboardButton("بازگشت", callback_data="return_show_available_conv_levels_dynamic")
        ]
    )
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "لطفا پارت مدنظر خود را انتخاب کنید:"

    await query.edit_message_text(text=text, reply_markup=reply_markup)
    return GET_NEW_TEXT_DYNAMIC




# GET_NEW_TEXT_DYNAMIC
async def get_new_text_dynamic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get("update_record") or context.user_data.get(
        'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user') or context.user_data.get('add_owner'):
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()

    query_data = query.data.split()[0]
    if query_data == "return_show_available_conv_levels_dynamic":
        return await show_available_conv_levels_dynamic(update, context)
    context.user_data["part_key"] = query_data


    # returning to previous step
    keyboard = [
        [
            InlineKeyboardButton("بازگشت", callback_data="return_show_available_parts_dynamic")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open("./dynamic_text.json", "r", encoding="utf-8") as t_file:
        content = json.load(t_file)
        current_text = content[context.user_data["conv_key"]][context.user_data["level_key"]][context.user_data["part_key"]]

    text = f"{current_text["text"]}\n\nلطفا متن مورد نظر خود را وارد کنید:\n\nمتغیر های دردسترس:\n{current_text["vars"]}"

    await query.edit_message_text(text=text, reply_markup=reply_markup)
    return EDIT_TEXT_DYNAMIC


# EDIT_TEXT_DYNAMIC
async def edit_text_dynamic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get(
        "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get("update_record") or context.user_data.get(
        'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user') or context.user_data.get('add_owner'):
        return ConversationHandler.END

    if update.callback_query and update.callback_query.data == "return_show_available_parts_dynamic":
        return await show_available_parts_dynamic(update, context)
    elif update.message:
        user_input = update.message.text
        try:
            with open("dynamic_text.json", "r", encoding="utf-8") as t_file:
                content = json.load(t_file)
                content[context.user_data["conv_key"]][context.user_data["level_key"]][context.user_data["part_key"]]["text"] = user_input
            with open("dynamic_text.json", "w", encoding="utf-8") as t_file:
                json.dump(content, t_file, ensure_ascii=False, indent=4)
            text = "عملیات با موفقیت انجام شد!"
        except Exception as e:
            text = "عملیات با خطا مواجه شد!"


        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return ConversationHandler.END



def dynamic_text_handler():
    dynamic_text_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^تغییر محتوای نوشته ها$"), dynamic_text_start)],
        states={
            SHOW_AVAILABLE_LEVELS_DYNAMIC: [
                MessageHandler(filters.Regex("^تغییر محتوای نوشته ها$"), dynamic_text_start),
                CallbackQueryHandler(show_available_conv_levels_dynamic, pattern=r"^.* -dt$"),
            ],
            SHOW_AVAILABLE_PARTS_DYNAMIC:[
                MessageHandler(filters.Regex("^تغییر محتوای نوشته ها$"), dynamic_text_start),
                CallbackQueryHandler(show_available_parts_dynamic, pattern=r"^.* -dt$"),
            ],
            GET_NEW_TEXT_DYNAMIC:[
                MessageHandler(filters.Regex("^تغییر محتوای نوشته ها$"), dynamic_text_start),
                CallbackQueryHandler(get_new_text_dynamic, pattern=r"^.* -dt|return_show_available_conv_levels_dynamic$"),
            ],
            EDIT_TEXT_DYNAMIC:[
                MessageHandler(filters.Regex("^تغییر محتوای نوشته ها$"), dynamic_text_start),
                CallbackQueryHandler(edit_text_dynamic, pattern=r"^return_show_available_parts_dynamic$"),
                MessageHandler(filters.TEXT, edit_text_dynamic),
            ]

        },
        fallbacks=[CommandHandler('done', admin_owner_panel_break_conversation)],
    )
    return dynamic_text_conv_handler