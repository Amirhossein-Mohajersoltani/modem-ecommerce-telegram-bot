from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CommandHandler, \
    CallbackQueryHandler
from utils import *
from database import *
import json



CARD_NUMBER = "546846635135464"



database = Database()




HANDLE_PAYMENT_FLOW, EDIT_ORDER_PAYMENT, DELETE_ORDER_PAYMENT , EDIT_COUNT_PAYMENT, GET_PHONE_PAYMENT, GET_ADDRESS_PAYMENT, REVIEW_PAYMENT, GET_DEPOSIT_DOC_PAYMENT = range(8)


# Start Point
async def payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not database.is_contain(update.effective_chat.id, "users", f"chat_id = {update.effective_chat.id}"):
        return ConversationHandler.END

    context.user_data.clear()
    context.user_data['payment_conv'] = True


    products = database.fetch_data('cart_items', f"chat_id = '{update.effective_chat.id}'")
    if products:
        context.user_data["user_cart"] = show_user_cart(products)
        text = context.user_data["user_cart"]["text"]
        keyboard = [
            [
                InlineKeyboardButton(
                    get_dynamic_text("payment","payment", "pay_option"),
                    callback_data="pay -p"
                ),
            ],
            [
                InlineKeyboardButton(
                    get_dynamic_text("payment","payment", "edit_option"),
                    callback_data="edit -p"
                ),
            ],
            [
                InlineKeyboardButton(
                    get_dynamic_text("payment","payment", "delete_option"),
                    callback_data="delete -p"
                ),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
    else:
        text = get_dynamic_text("payment","payment", "no_cart")
        reply_markup = None
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
        return ConversationHandler.END

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
    return HANDLE_PAYMENT_FLOW

# HANDLE_PAYMENT_FLOW
async def get_id_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # singular conv checker
    if context.user_data.get('update_user_info_conv') or context.user_data.get('simcard_conv') or context.user_data.get('modem_conv'):
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()


    reply_markup = create_user_break_button()
    text = get_dynamic_text("payment", "get_id_payment", "message")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)

    if query.data == "edit -p":
        return EDIT_ORDER_PAYMENT
    elif query.data == "delete -p":
        return DELETE_ORDER_PAYMENT




# EDIT_ORDER_PAYMENT
async def edit_order_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # singular conv checker
    if context.user_data.get('update_user_info_conv') or context.user_data.get('simcard_conv') or context.user_data.get('modem_conv'):
        return ConversationHandler.END

    # user input validation
    user_input = convert_numbers(update.message.text).strip()

    if not is_valid_number(user_input):
        await update.message.reply_text(get_dynamic_text("payment", "edit_order_payment", "invalid_user_input"))
        return EDIT_ORDER_PAYMENT
    else:
        flag = False
        for order in context.user_data["user_cart"]["orders"]:
            order_id = order["order_data"]["order_id"]
            if int(order_id) == int(user_input):
                flag = True
        if not flag:
            await update.message.reply_text(get_dynamic_text("payment", "edit_order_payment", "invalid_order_id"))
            return EDIT_ORDER_PAYMENT


    context.user_data["order_id"] = int(user_input)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=get_dynamic_text("payment", "edit_order_payment", "message")
    )
    return EDIT_COUNT_PAYMENT



# EDIT_COUNT_PAYMENT
async def edit_count_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # singular conv checker
    if context.user_data.get('update_user_info_conv') or context.user_data.get('simcard_conv') or context.user_data.get('modem_conv'):
        return ConversationHandler.END

    # Determine the order count
    user_input = convert_numbers(update.message.text).strip()


    if not is_valid_number(user_input):
        await update.message.reply_text("❌ مقدار نامعتبر است! لطفا یک عدد معتبر وارد کنید:")
        return EDIT_COUNT_PAYMENT
    else:
        for order in context.user_data["user_cart"]["orders"]:
            order_id = order["order_data"]["order_id"]
            if context.user_data["order_id"] == order_id:
                product_table = order["product_data"]["product_table"]
                product_id =int(order["product_data"]["product_id"])
                product_data = database.fetch_data(product_table, f"id = '{product_id}'")
                if product_table == "modem":
                    product_inventory = product_data[0][5]
                elif product_table == "simcard":
                    product_inventory = product_data[0][4]
        if int(user_input) > product_inventory:
            await update.message.reply_text(
                f"متاسفانه از این کالا به تعداد {product_inventory} موجود می باشد. لطفا مقدار کمتری وارد کنید:")
            return EDIT_COUNT_PAYMENT


    count = int(user_input)
    record = Record(table_name="cart_items", product_count=count)
    reply_markup = create_user_panel()
    if database.update_record(record , f"id = '{context.user_data["order_id"]}'"):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=get_dynamic_text("payment", "edit_count_payment", "success_message"),
            reply_markup=reply_markup
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=get_dynamic_text("payment", "edit_count_payment", "failed_message"),
            reply_markup=reply_markup
        )

    return await payment(update, context)



# DELETE_ORDER_PAYMENT
async def delete_order_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # singular conv checker
    if context.user_data.get('update_user_info_conv') or context.user_data.get('simcard_conv') or context.user_data.get('modem_conv'):
        return ConversationHandler.END

    # user input validation
    user_input = convert_numbers(update.message.text).strip()

    if not is_valid_number(user_input):
        await update.message.reply_text("❌ مقدار نامعتبر است! لطفا یک عدد معتبر وارد کنید:")
        return DELETE_ORDER_PAYMENT
    else:
        flag = False
        for order in context.user_data["user_cart"]["orders"]:
            order_id = int(order["order_data"]["order_id"])
            if order_id == int(user_input):
                flag = True
        if not flag:
            await update.message.reply_text("❌ مقدار نامعتبر است! لطفا شماره سفارش معتبر وارد کنید:")
            return DELETE_ORDER_PAYMENT

    order_id = user_input
    reply_markup = create_user_panel()
    if database.delete_record("cart_items", f"id = '{order_id}'"):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=get_dynamic_text("payment", "delete_order_payment", "success_message"),
            reply_markup=reply_markup
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=get_dynamic_text("payment", "delete_order_payment", "failed_message"),
            reply_markup=reply_markup
        )

    return await payment(update, context)





# CHECK_USER_DATA_PAYMENT
async def check_user_data_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # singular conv checker
    if context.user_data.get('update_user_info_conv') or context.user_data.get('simcard_conv') or context.user_data.get('modem_conv'):
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()

    # Check for a detail for customer
    result = database.fetch_data("users", f" chat_id = '{update.effective_chat.id}'")
    context.user_data["chat_id"] = update.effective_chat.id
    if not result[0][2] or not result[0][4] or not result[0][5]:
        context.user_data['info-pass'] = False
        reply_markup = create_break_button()
        await context.bot.send_message(chat_id=update.effective_chat.id, text="لطفا نام و نام خانوادگی خود را وارد کنید:",reply_markup=reply_markup)
        return GET_PHONE_PAYMENT
    else:
        context.user_data['full_name'] = result[0][2]
        context.user_data['phone'] = result[0][4]
        context.user_data['address'] = result[0][5]
        context.user_data['info-pass'] = True
        return await review_payment(update, context)



# GET_PHONE_PAYMENT
async def get_phone_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # singular conv checker
    if context.user_data.get('update_user_info_conv') or context.user_data.get('simcard_conv') or context.user_data.get('modem_conv'):
        return ConversationHandler.END

    user_input = update.message.text

    if not is_valid_name(user_input):
        await update.message.reply_text("❌ نام وارد شده نامعتبر است! لطفا فقط از حروف فارسی یا لاتین استفاده کنید:")
        return GET_PHONE_PAYMENT

    context.user_data['full_name'] = user_input
    context.user_data['username'] = user_input
    await context.bot.send_message(chat_id=update.effective_chat.id, text="لطفا شماره تماس خود را وارد کنید:")
    return GET_ADDRESS_PAYMENT




# GET_ADDRESS_PAYMENT
async def get_address_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # singular conv checker
    if context.user_data.get('update_user_info_conv') or context.user_data.get('simcard_conv') or context.user_data.get('modem_conv'):
        return ConversationHandler.END

    user_input = convert_numbers(update.message.text).strip()

    if not is_valid_phone(user_input):
        await update.message.reply_text("❌ شماره تماس نامعتبر است! لطفا شماره‌ای ۱۱ رقمی که با ۰۹ شروع می‌شود، وارد کنید:")
        return GET_ADDRESS_PAYMENT

    context.user_data['phone'] = user_input
    await context.bot.send_message(chat_id=update.effective_chat.id, text="لطفا آدرس پستی خود را وارد کنید:")
    return REVIEW_PAYMENT



# BUY_REVIEW
async def review_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # singular conv checker
    if context.user_data.get('update_user_info_conv') or context.user_data.get('simcard_conv') or context.user_data.get('modem_conv'):
        return ConversationHandler.END

    if not context.user_data['info-pass']:
        user_input = update.message.text

        if not is_valid_address(user_input):
            await update.message.reply_text("❌ آدرس خیلی کوتاه است! لطفا یک آدرس کامل وارد کنید:")
            return REVIEW_PAYMENT

        context.user_data['address'] = user_input
        # update record with new data
        record = Record(table_name="users", phone=context.user_data['phone'], address=context.user_data['address'],
                    username=context.user_data['username'])
        database.update_record(record, f" chat_id = '{update.effective_chat.id}'")


    # add user data to user_cart
    context.user_data["user_cart"]["user_data"] = {
        "chat_id": update.effective_chat.id,
        "full_name": context.user_data["full_name"],
        "phone": context.user_data["phone"],
        "address": context.user_data["address"]
    }


    context.user_data["user_cart"]["card_number"] = CARD_NUMBER


    # تولید متن تایید سفارش
    additional_data = {
        "{order_text}": context.user_data["user_cart"]["text"],
        "{full_name}": context.user_data['full_name'],
        "{phone}": context.user_data['phone'],
        "{address}": context.user_data['address'],
        "{total_price}": context.user_data["user_cart"]["total_price"],
        "{card_number}": CARD_NUMBER
    }
    text = get_dynamic_text("payment", "review_payment", "message", additional_data)
    reply_markup = create_break_button()


    await context.bot.send_message(chat_id=update.effective_chat.id, text=text,reply_markup=reply_markup)
    return GET_DEPOSIT_DOC_PAYMENT




# GET_DEPOSIT_DOC_PAYMENT
async def get_deposit_doc_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # singular conv checker
    if context.user_data.get('update_user_info_conv') or context.user_data.get('simcard_conv') or context.user_data.get('modem_conv'):
        return ConversationHandler.END

    # Check for input Validation and save image id
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        context.user_data["user_cart"]["deposit_image_id"] = file_id
    elif update.message.text:
        context.user_data["user_cart"]["deposit_text"] = update.message.text


    # update product inventory
    for order in context.user_data["user_cart"]["orders"]:
        product_table = order["product_data"]["product_table"]
        product_id = order["product_data"]["product_id"]
        order_count = order["order_data"]["order_count"]
        # Fetch inventory
        if product_table == "modem":
            inventory = database.fetch_data("modem", f"id = '{product_id}'")[0][5]
        else:
            inventory = database.fetch_data("simcard", f"id = '{product_id}'")[0][4]
        new_inventory = inventory - order_count
        # Save new inventory
        record = Record(table_name=product_table,product_count=new_inventory)
        database.update_record(record, f"id = '{product_id}'")


    # add to database
    json_cart = json.dumps(context.user_data["user_cart"], ensure_ascii=False)
    record = Record(table_name="pending_approval", cart=json_cart)
    if database.add_record(record):
        # Delete orders from 'cart_items' table:
        database.delete_record("cart_items", f"chat_id = '{context.user_data["user_cart"]["user_data"]["chat_id"]}'")

        # Send Received Message
        reply_markup = create_user_panel()
        text = "✅ سفارش شما ثبت شد. تیم پشتیبانی به زودی با شما تماس خواهد گرفت."
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
    else:
        reply_markup = create_user_panel()
        text = "✅ مشکلی در ثبت سفارش پیش آمده. لطفا با تیم پشتیبانی تماس بگیرید."
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)


    return ConversationHandler.END

# HANDLE_PAYMENT_FLOW, EDIT_ORDER_PAYMENT, DELETE_ORDER_PAYMENT , EDIT_COUNT_PAYMENT, GET_PHONE_PAYMENT, GET_ADDRESS_PAYMENT, REVIEW_PAYMENT, GET_DEPOSIT_DOC_PAYMENT
# Handler
def buy_handler():
    buy_conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex("^نمایش سبد خرید$"),payment)
        ],
        states={
            HANDLE_PAYMENT_FLOW: [
                MessageHandler(filters.Regex("^نمایش سبد خرید$"), payment),
                CallbackQueryHandler(check_user_data_payment, pattern="^pay -p$"),
                CallbackQueryHandler(get_id_payment, pattern="^(edit|delete) -p$"),
            ],
            EDIT_ORDER_PAYMENT:[
                MessageHandler(filters.Regex("^نمایش سبد خرید$"), payment),
                MessageHandler(filters.Regex("^لغو عملیات!$"), user_panel_break_conversation),
                MessageHandler(filters.TEXT & ~filters.COMMAND, edit_order_payment)
            ],
            EDIT_COUNT_PAYMENT: [
                MessageHandler(filters.Regex("^نمایش سبد خرید$"), payment),
                MessageHandler(filters.Regex("^لغو عملیات!$"), user_panel_break_conversation),
                MessageHandler(filters.TEXT & ~filters.COMMAND, edit_count_payment)
            ],
            DELETE_ORDER_PAYMENT: [
                MessageHandler(filters.Regex("^نمایش سبد خرید$"), payment),
                MessageHandler(filters.Regex("^لغو عملیات!$"), user_panel_break_conversation),
                MessageHandler(filters.TEXT & ~filters.COMMAND, delete_order_payment)
            ],
            GET_PHONE_PAYMENT: [
                MessageHandler(filters.Regex("^نمایش سبد خرید$"), payment),
                MessageHandler(filters.Regex("^لغو عملیات!$"), user_panel_break_conversation),
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone_payment)
            ],
            GET_ADDRESS_PAYMENT: [
                MessageHandler(filters.Regex("^نمایش سبد خرید$"), payment),
                MessageHandler(filters.Regex("^لغو عملیات!$"), user_panel_break_conversation),
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_address_payment)
            ],
            REVIEW_PAYMENT: [
                MessageHandler(filters.Regex("^نمایش سبد خرید$"), payment),
                MessageHandler(filters.Regex("^لغو عملیات!$"), user_panel_break_conversation),
                MessageHandler(filters.TEXT & ~filters.COMMAND, review_payment)
            ],
            GET_DEPOSIT_DOC_PAYMENT: [
                MessageHandler(filters.Regex("^نمایش سبد خرید$"), payment),
                MessageHandler(filters.Regex("^لغو عملیات!$"), user_panel_break_conversation),
                MessageHandler(filters.PHOTO | filters.TEXT & ~filters.COMMAND, get_deposit_doc_payment)
            ]
        },
        fallbacks=[CommandHandler('done', user_panel_break_conversation)],
    )

    return buy_conv_handler




def show_user_cart(products):
    counter = 1
    user_cart = {
        "text": "",
        "total_price": 0,
        "card_number": None,
        "deposit_image_id": None,
        "deposit_text": None,
        "user_data": {},
        "orders": []
    }
    text = get_dynamic_text("payment","payment","order_head")
    total_price = 0
    for product in products:
        # preparing additional data
        order_id = product[0]
        product_table = product[1]
        product_id = product[2]
        order_count = product[3]

        product_record = database.fetch_data(table_name=product_table, condition=f"id = '{product_id}'")
        product_name = product_record[0][2]
        product_model = product_record[0][1]

        if product_table == "simcard":
            price = product_record[0][5]
            order_total_price = price * order_count
            product_situation = None
            additional_data = {
                "{counter}": counter,
                "{product_name}": product_name,
                "{order_id}": order_id,
                "{order_count}": order_count,
                "{price}": price,
                "{order_total_price}": order_total_price
            }
            p_text = get_dynamic_text("payment","payment","order_template_simcard",additional_data=additional_data) + "\n"

        elif product_table == "modem":
            if product_record[0][3]:
                product_situation = "آکبند"
            else:
                product_situation = "استوک"

            price = product_record[0][4]
            order_total_price = price * order_count
            additional_data = {
                "{counter}": counter,
                "{product_name}": product_name,
                "{order_id}": order_id,
                "{order_count}": order_count,
                "{price}": price,
                "{product_situation}": product_situation,
                "{order_total_price}": order_total_price
            }

            p_text = get_dynamic_text("payment", "payment", "order_template_modem",additional_data=additional_data) + "\n"

        user_cart["orders"].append(
            {
                "product_data": {
                    "product_table": product_table,
                    "product_id": product_id,
                    "product_name": product_record[0][2],
                    "product_model": product_model,
                    "product_price": price,
                    "product_situation": product_situation,
                },
                "order_data": {
                    "order_id": order_id,
                    "order_name": product_name,
                    "order_count": order_count,
                    "order_total_price": price * order_count,
                }
            }
        )


        total_price += price * order_count
        text += p_text
        counter += 1



    additional_data = {"{total_price}": total_price}
    footer = get_dynamic_text("payment", "payment", "order_footer",additional_data=additional_data)
    text += footer
    user_cart["text"] = text
    user_cart["total_price"] = total_price
    return user_cart

