from lib2to3.fixes.fix_input import context

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler


async def say_hello(update: Update, context: CallbackContext):


    # active one conversation per moment
    if context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get("delete_product") or context.user_data.get("dynamic_text") or context.user_data.get("pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get("show_product") or context.user_data.get("update_record"):
        return ConversationHandler.END

    return ConversationHandler.END





#
# # Read scv
#     try:
#         df = pd.read_csv("./data/pending_approval.csv", encoding="utf-8")
#     except FileNotFoundError:
#         df = pd.DataFrame(columns=[
#             'chat_id', 'product_table', 'product_id',
#             'product_name', 'product_count', 'product_situation', 'total_price',
#             'username', 'phone', 'address', 'card_number', 'deposit_image_id'
#         ])
#
#     # اضافه کردن رکورد جدید
#     new_record = {
#         'chat_id': context.user_data["chat_id"],
#         'product_table': context.user_data.get("table"),
#         'product_id': context.user_data.get("id"),
#         'product_name': context.user_data.get("product_name"),
#         'product_count': context.user_data.get("product_count"),
#         'product_situation': context.user_data.get("product_situation"),
#         'total_price': context.user_data.get("total_price"),
#         'username': context.user_data.get("username"),
#         'phone': context.user_data.get("phone"),
#         'address': context.user_data.get("address"),
#         'card_number': CARD_NUMBER,
#         'deposit_image_id': context.user_data.get("deposit_image_id")
#     }
#
#     df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
#
#     # Save in csv file
#     df.to_csv("./data/pending_approval.csv", index=False, encoding="utf-8")
#
#     # update product inventory
#     new_inventory = context.user_data["product_inventory"] - context.user_data.get("product_count")
#     record = Record(table_name=context.user_data.get("table"), product_count=new_inventory)
#     if database.update_record(record, f" id = {context.user_data.get("id")}"):
#         # Send Received Message
#         reply_markup = create_user_panel()
#         text = "✅ سفارش شما ثبت شد. تیم پشتیبانی به زودی با شما تماس خواهد گرفت."
#         await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
#     else:
#         reply_markup = create_user_panel()
#         text = "✅ مشکلی در ثبت سفارش پیش آمده. لطفا با تیم پشتیبانی تماس بگیرید."
#         await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
#
#
#     return ConversationHandler.END