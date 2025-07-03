# async def caps_format(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     text_caps = ' '.join(context.args).upper()
#     await application.updater.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
#
# async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.inline_query.query
#     if not query:
#         return
#     results = []
#     results.append(
#         InlineQueryResultArticle(
#             id=str(uuid4()),
#             title='Send Hello',
#             input_message_content=InputTextMessageContent("Hello World!"),
#         )
#     )
#     await context.bot.answer_inline_query(update.inline_query.id, results)



# ---------------------------
# caps_handler = CommandHandler('caps', caps_format)
# application.add_handler(caps_handler)
#
# inline_caps_handler = InlineQueryHandler(inline_caps)
# application.add_handler(inline_caps_handler)

# ----------------------------------------------------------------------------------------------------------------

# elif update.message.text == "خرید سیمکارت":
# text = "یه چیزی"
# else:
# text = "لطفا از منوی زیر گزینه دلخواه خود را انتخاب کنید."
#
# try:
#     reply_markup = InlineKeyboardMarkup(keyboard)
# except NameError:
#     reply_markup = None
#
# if not None and None:
#     print("Hello")
# import pymysql
#
# # اطلاعات اتصال به دیتابیس
# db_config = {
#     "host": "188.34.178.143",
#     "user": "amirhossein",
#     "password": "g9x76Z!8W]Co1",
#     "database": "modem",
# }
#
# # اتصال به دیتابیس
# connection = pymysql.connect(**db_config)
#
#

#
# try:
#     with connection.cursor() as cursor:
#         # بررسی اینکه ستون address وجود دارد یا نه
#         cursor.execute("SHOW COLUMNS FROM users LIKE 'address';")
#         result = cursor.fetchone()
#         if not result:
#             # اضافه کردن ستون address اگر وجود نداشته باشد
#             cursor.execute("ALTER TABLE users ADD COLUMN address VARCHAR(255) NULL;")
#             print("ستون address اضافه شد.")
#         else:
#             print("ستون address از قبل وجود دارد.")
#
#         # تغییر ستون‌های دیگر برای پذیرش NULL
#         cursor.execute("ALTER TABLE users MODIFY full_name VARCHAR(255) NULL;")
#         cursor.execute("ALTER TABLE users MODIFY phone_number VARCHAR(15) NULL;")
#         print("تغییر ستون‌های دیگر انجام شد.")
#
#     # اعمال تغییرات
#     connection.commit()
#     print("تمام تغییرات با موفقیت انجام شد.")
#
# except Exception as e:
#     print("خطا در اجرای دستورات:", e)
#
# finally:
#     connection.close()


# if 1:
#     print(1 == True)
# import database
#
# database = database.Database()
#
# result = database.fetch_data("modem", "model = '5G' and is_new = true")
#
#
# for i in result:
#     print(i[3])


#
# m = ((6, '5G', 'یک نام', 0, 3871624, 7, '0', 'توضیح'), (7, '5G', 'لتلبی', 0, 57843, 9, '0', 'لیبتنمولیس'), (8, '4G', 'Fjhsvskkc', 0, 1000, 20, '0', 'Vsksksghdjfkdkjd'), (9, 'TD-LTE', 'مودم TD-LTE مبین نت', 0, 5400000, 78, '0', 'مودم خوب که از سیمکارت همراه اول استفاده میکنه'), (11, '5G', 'مودم خیلی سریع', 1, 123456, 2, '0', 'متن توضیحات سریع'), (12, '4G', 'D-Link 953', 0, 1870000, 0, '0', 'مودم FD، با آنتن دهی قوی، مناسب برای انتقال تصویر و مناطق با پوشش آنتن ضعیف'), (13, '4G', 'FD-i40 B2 (K-Link)', 1, 2200000, 20, 'AgACAgQAAxkBAAOxZ-gowXP1nmhl4yOVV-zfnM8kFKkAAoXGMRuc10FT0eopn8JdLLgBAAMCAAN4AAM2BA', '✅مودم FD(4G,3G)، دارای 2 آنتن خارجی\n✅ دارای 3 پورت LAN\n✅دارای ورودی تغذیه تایپ C\n✅ توانایی ارتباط تا 150Mbps\n✅توانایی اتصال همزمان تا 16 نفر\n✅مناسب جهت انتقال تصویر و مصرف خانگی'))
#
#
# for modem in m:
#     print(modem[5])

#
import database



datab = database.Database()



# print(datab.delete_record("pending_approval", f"id = '1'"))

print(datab.fetch_data("cart_items"))
