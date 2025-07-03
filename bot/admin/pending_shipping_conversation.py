from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ConversationHandler, ContextTypes, MessageHandler, filters, CommandHandler, \
    CallbackQueryHandler
from bot.core.database import *
from bot.core.utils import *
import pandas as pd
import json

database = Database()

# States
SHIPPING = range(1)


# Start Point
async def start_shipping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if database.is_admin(update.effective_chat.id) or database.is_owner(update.effective_chat.id):
        context.user_data.clear()
        context.user_data["pending_shipping"] = True
        # Read Database
        result = database.fetch_data("pending_shipping")

        if not result:
            text = "هیچ سفارشی یافت نشد."
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
            return ConversationHandler.END

        else:

            keyboard = [
                [
                    InlineKeyboardButton("ارسال شد!", callback_data="shipped -ps"),
                ],
                [
                    InlineKeyboardButton("خروج", callback_data="exit -ps"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            first_row = result[0]
            user_cart = json.loads(first_row[1])
            date = first_row[2]

            # 'chat_id', 'product_table', 'product_id',
            # 'product_name', 'product_count', 'product_situation', 'total_price',
            # 'username', 'phone', 'address', 'card_number', 'deposit_image_id'

            # save user cart
            context.user_data["user_cart"] = user_cart
            context.user_data["user_cart_id"] = first_row[0]
            # constant data
            # user data
            context.user_data['chat_id'] = user_cart["user_data"]["chat_id"]
            context.user_data['full_name'] = user_cart["user_data"]["full_name"]
            context.user_data['phone'] = user_cart["user_data"]["phone"]
            context.user_data['address'] = user_cart["user_data"]["address"]
            # card number
            context.user_data['card_number'] = user_cart["card_number"]
            # orders
            context.user_data['order_text'] = user_cart["text"]
            context.user_data['total_price'] = user_cart["total_price"]
            context.user_data['deposit_image_id'] = user_cart["deposit_image_id"]
            context.user_data['deposit_text'] = user_cart["deposit_text"]
            # date
            context.user_data["order_date"] = date

            text = (
                f"📦 سفارش جدید درانتظار ارسال!\n\n"
                f"👤 نام مشتری: {context.user_data['full_name']}\n"
                f"📞 شماره تماس: {context.user_data['phone']}\n"
                f"📍 آدرس: {context.user_data['address']}\n"
                f"📌 محصولات: {context.user_data['order_text']}\n"
            )

            if context.user_data['deposit_image_id']:
                try:
                    await context.bot.send_photo(
                        chat_id=update.effective_chat.id,
                        photo=user_cart["deposit_image_id"],
                        caption=text,
                        reply_markup=reply_markup
                    )
                except Exception as e:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=text,
                        reply_markup=reply_markup
                    )

            elif context.user_data['deposit_text']:
                text += f"\n\nرسید پرداخت:\n{context.user_data['deposit_text']}"
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=text,
                    reply_markup=reply_markup
                )
            return SHIPPING
    return ConversationHandler.END



# SHIPPING
async def shipp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
        "pending_approval") or context.user_data.get(
        "show_product") or context.user_data.get("update_record") or context.user_data.get(
        'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user') or context.user_data.get('add_owner'):
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()

    if query.data == 'shipped -ps':

        user_cart = context.user_data["user_cart"]
        json_cart = json.dumps(user_cart, ensure_ascii=False)
        record = Record(table_name="completed_orders", cart=json_cart)
        if database.add_record(record):
            database.delete_record("pending_shipping", f"id = '{context.user_data["user_cart_id"]}'")

        if query:
            await query.delete_message()
        else:
            await context.bot.delete_message(chat_id=update.effective_chat.id,
                                             message_id=update.effective_message.message_id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="ارسال تایید شد!")

        text = "سفارش شما ارسال شد!"
        await context.bot.send_message(chat_id=context.user_data["chat_id"], text=text)

        return await start_shipping(update, context)

    elif query.data == 'exit -ps':
        await query.delete_message()
        await context.bot.send_message(chat_id=update.effective_chat.id, text="عملیات لغو شد!")
        return ConversationHandler.END



# Pending Shipping Conversation Handler
def pending_shipping():
    pending_shipping_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^لیست سفارش های در انتظار ارسال$"), start_shipping)],
        states={
            SHIPPING: [CallbackQueryHandler(shipp, pattern="^(shipped|exit) -ps$")],
        },
        fallbacks = [CommandHandler('done', admin_owner_panel_break_conversation)]
    )
    return pending_shipping_conv_handler



