from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ConversationHandler, ContextTypes, MessageHandler, filters, CommandHandler, \
    CallbackQueryHandler
from bot.core.database import *
from bot.core.utils import *
from pending_shipping_conversation import start_shipping

import json

database = Database()


# States
AUTHENTICATING = range(1)



# Start Point
async def start_approval(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if database.is_admin(update.effective_chat.id) or database.is_owner(update.effective_chat.id):
        context.user_data.clear()
        context.user_data["pending_approval"] = True

        # Read Database
        result = database.fetch_data("pending_approval")

        if not result:
            text = "هیچ سفارشی یافت نشد."
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
            return ConversationHandler.END

        else:

            keyboard = [
                [
                    InlineKeyboardButton("تایید", callback_data="approve -pa"),
                ],
                [
                    InlineKeyboardButton("رد", callback_data="decline -pa"),
                ],
                [
                    InlineKeyboardButton("خروج", callback_data="exit -pa"),
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
            print(user_cart["user_data"])
            print(user_cart)
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




            # context.user_data['product_table'] = first_row['product_table']
            # context.user_data['product_id'] = first_row['product_id']
            #
            # context.user_data['product_name'] = first_row['product_name']
            # context.user_data['product_count'] = first_row['product_count']
            # context.user_data['product_situation'] = first_row['product_situation']
            # context.user_data['total_price'] = first_row['total_price']
            #
            #
            # context.user_data['deposit_image_id'] = first_row['deposit_image_id']



            text = (
                f"📦 سفارش جدید ثبت شد!\n\n"
                f"{context.user_data['order_text']}"
            )


            if context.user_data['deposit_image_id']:
                try:
                    await context.bot.send_photo(
                        chat_id=update.effective_chat.id,
                        photo= context.user_data["user_cart"]['deposit_image_id'],
                        caption=text,
                        reply_markup=reply_markup
                    )
                except Exception as e:
                    return await authenticating(update, context)


            elif context.user_data['deposit_text']:
                text += f"\n\nرسید پرداخت:\n{context.user_data['deposit_text']}"
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text = text,
                    reply_markup =reply_markup
                )


            return AUTHENTICATING
    return ConversationHandler.END



# AUTHENTICATING
async def authenticating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # active one conversation per moment
    if (context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
            "delete_product") or context.user_data.get("dynamic_text")
            or context.user_data.get("pending_shipping") or context.user_data.get(
        "show_product") or context.user_data.get("update_record") or context.user_data.get(
        'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
        'delete_user') or context.user_data.get('add_owner')):
        return ConversationHandler.END

    query = update.callback_query

    if query:
        await query.answer()
        data = query.data
    else:
        data = "decline -pa"

    if data == 'approve -pa':
        # Save data in pending shipping
        user_cart = context.user_data["user_cart"]
        json_cart = json.dumps(user_cart, ensure_ascii=False)
        record = Record(table_name="pending_shipping", cart=json_cart)
        result = database.add_record(record)
        print(result)
        if result:
            # Decrease the inventory:
            flag = True
            # for order in user_cart["orders"]:
            #     product_table = order["product_data"]["product_table"]
            #     product_id = order["product_data"]["product_id"]
            #     order_count = order["order_data"]["order_count"]
            #     product_record = database.fetch_data(product_table, f"id = '{product_id}'")[0]
            #     if product_table == "modem":
            #         product_inventory = product_record[5]
            #     else:
            #         product_inventory = product_record[4]
            #     new_inventory = product_inventory - order_count
            #
            #     update_inventory_record = Record(table_name=product_table,product_count=new_inventory)
            #     if not database.update_record(update_inventory_record, f"id = '{product_id}'"):
            #         flag = False

            # Delete the Row
            if flag:
                database.delete_record("pending_approval", f"id = '{context.user_data["user_cart_id"]}'")

            if query:
                await query.delete_message()
            else:
                await context.bot.delete_message(chat_id=update.effective_chat.id,
                                                 message_id=update.effective_message.message_id)
            await query.message.chat.send_message("سفارش تایید شد!")

            text = "سفارش شما تایید شد!"
            await context.bot.send_message(chat_id=context.user_data['chat_id'], text=text)

            return await start_approval(update, context)

    elif data == 'decline -pa' :
        # increase the inventory
        user_cart = context.user_data["user_cart"]
        for order in user_cart["orders"]:
            product_table = order["product_data"]["product_table"]
            product_id = order["product_data"]["product_id"]
            order_count = order["order_data"]["order_count"]
            product_record = database.fetch_data(product_table, f"id = '{product_id}'")[0]
            if product_table == "modem":
                product_inventory = product_record[5]
            else:
                product_inventory = product_record[4]
            new_inventory = product_inventory + order_count

            update_inventory_record = Record(table_name=product_table, product_count=new_inventory)
            database.update_record(update_inventory_record, f"id = '{product_id}'")


        json_cart = json.dumps(user_cart, ensure_ascii=False)
        declined_record = Record(table_name="declined_orders", cart=json_cart)
        database.add_record(declined_record)

        # Delete record
        database.delete_record("pending_approval", f"id = '{context.user_data["user_cart_id"]}'")


        if query:
            await query.delete_message()
        else:
            await context.bot.delete_message(chat_id=update.effective_chat.id,
                                             message_id=update.effective_message.message_id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="سفارش رد شد!")


        text = "سفارش شما رد شد!\n درصورت بروز مشکل لطفا با پشتیبانی تماس حاصل فرمایید:\n @id_backup"
        await context.bot.send_message(chat_id=int(context.user_data["chat_id"]), text=text)
        return await start_approval(update, context)



    elif data == 'exit -pa':
        await query.delete_message()
        await context.bot.send_message(chat_id=update.effective_chat.id, text="عملیات لغو شد!")
        return ConversationHandler.END



# Pending Approval Conversation Handler
def pending_approval():
    pending_approval_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^لیست سفارش های در انتظار تایید$"), start_approval)],
        states={
            AUTHENTICATING: [CallbackQueryHandler(authenticating, pattern="^(approve|decline|exit) -pa$")],
        },
        fallbacks = [CommandHandler('done', admin_owner_panel_break_conversation)]
    )
    return pending_approval_conv_handler



