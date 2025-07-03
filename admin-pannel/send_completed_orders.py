import pandas as pd
from telegram import Update, InputFile
from telegram.ext import ContextTypes
from database import *
import json
import os

database = Database()

async def send_completed_orders(update, context: ContextTypes.DEFAULT_TYPE):
    if database.is_admin(update.effective_user.id) or database.is_owner(update.effective_user.id):
        data = database.fetch_data("completed_orders")

        if not data:
            await update.message.reply_text("هیچ سفارش تکمیل‌شده‌ای یافت نشد.")
            return

        rows = []
        for row in data:
            order_id, cart_json, date = row
            try:
                cart = json.loads(cart_json)
            except json.JSONDecodeError:
                continue  # skip invalid JSON

            user_info = cart.get("user_data", {})
            orders = cart.get("orders", [])

            for order in orders:
                product = order.get("product_data", {})
                order_data = order.get("order_data", {})
                rows.append({
                    "Order ID": order_data.get("order_id"),
                    "Product Table": product.get("product_table"),
                    "Product ID": product.get("product_id"),
                    "Product Name": product.get("product_name"),
                    "Product Model": product.get("product_model"),
                    "Price (Single)": product.get("product_price"),
                    "Count": order_data.get("order_count"),
                    "Total Price": order_data.get("order_total_price"),
                    "Situation": product.get("product_situation"),
                    "Customer Name": user_info.get("full_name"),
                    "Phone": user_info.get("phone"),
                    "Address": user_info.get("address"),
                    "Card Number": cart.get("card_number"),
                    "Date": date.strftime('%Y-%m-%d %H:%M:%S'),
                })

        # Convert rows to DataFrame
        df = pd.DataFrame(rows)

        # Save the DataFrame to a CSV file
        filename_csv = "completed_orders.csv"
        df.to_csv(filename_csv, index=False, encoding='utf-8-sig')

        # Send the CSV file
        with open(filename_csv, 'rb') as file:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=file,
                filename='completed_orders.csv'
            )

        # Remove the temporary CSV file after sending it
        os.remove(filename_csv)


# async def send_completed_orders(update:Update,context:ContextTypes.DEFAULT_TYPE):
#     if database.is_admin(update.effective_user.id):
#         data = database.fetch_data("completed_orders")
#
#         if not data:
#             await update.message.reply_text("هیچ سفارش تکمیل‌شده‌ای یافت نشد.")
#             return
#
#         rows = []
#         for row in data:
#             order_id, cart_json, date = row
#             try:
#                 cart = json.loads(cart_json)
#             except json.JSONDecodeError:
#                 continue  # skip invalid JSON
#
#             user_info = cart.get("user_data", {})
#             orders = cart.get("orders", [])
#
#             for order in orders:
#                 product = order.get("product_data", {})
#                 order_data = order.get("order_data", {})
#                 rows.append({
#                     "Order ID": order_data.get("order_id"),
#                     "Product Table": product.get("product_table"),
#                     "Product ID": product.get("product_id"),
#                     "Product Name": product.get("product_name"),
#                     "Product Model": product.get("product_model"),
#                     "Price (Single)": product.get("product_price"),
#                     "Count": order_data.get("order_count"),
#                     "Total Price": order_data.get("order_total_price"),
#                     "Situation": product.get("product_situation"),
#                     "Customer Name": user_info.get("full_name"),
#                     "Phone": user_info.get("phone"),
#                     "Address": user_info.get("address"),
#                     "Card Number": cart.get("card_number"),
#                     "Date": date.strftime('%Y-%m-%d %H:%M:%S'),
#                 })
#         filename = "completed_orders.csv"
#         with open(filename, mode="w", encoding="utf-8", newline="") as file:
#             writer = csv.DictWriter(file, fieldnames=rows[0].keys())
#             writer.writeheader()
#             writer.writerows(rows)
#             file.flush()
#             os.fsync(file.fileno())
#
#         await context.bot.send_document(
#             chat_id=update.effective_chat.id,
#             document=InputFile(filename, filename="completed_orders.csv"),
#             caption="لیست سفارش‌های تکمیل‌شده",
#         )
#         await asyncio.sleep(1)
#         os.remove(filename)