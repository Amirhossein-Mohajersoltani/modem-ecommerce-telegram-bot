# import pymysql
#
# # اتصال به دیتابیس
# connection = pymysql.connect(
#     host="188.34.178.143",
#     user="amirhossein",
#     password="g9x76Z!8W]Co1",
#     database="modem",
#     charset='utf8mb4',
#     cursorclass=pymysql.cursors.DictCursor
# )
#
# try:
#     with connection.cursor() as cursor:
#         # مرحله ۱: تبدیل داده‌ها به عدد صحیح
#         update_query = """
#         UPDATE simcard
#         SET price = FLOOR(price);
#         """
#         cursor.execute(update_query)
#         print("مقادیر price به عدد صحیح تبدیل شدند.")
#
#         # مرحله ۲: تغییر نوع ستون به INT
#         alter_query = """
#         ALTER TABLE simcard
#         MODIFY COLUMN price INT;
#         """
#         cursor.execute(alter_query)
#         print("نوع ستون price به INT تغییر یافت.")
#
#     # نهایی کردن تغییرات
#     connection.commit()
#
# except pymysql.MySQLError as e:
#     print(f"خطا در انجام عملیات: {e}")
#
# finally:
#     connection.close()
#     print("اتصال به دیتابیس بسته شد.")


# import pymysql
#
# # Database connection configuration
# db_config = {
#     'host': '188.34.178.143',
#     'user': 'amirhossein',
#     'password': 'g9x76Z!8W]Co1',
#     'database': 'modem'
# }
#
# # Connect to the database
# connection = pymysql.connect(**db_config)
#
# try:
#     with connection.cursor() as cursor:
#         # List of tables to modify
#         tables = [
#             'pending_approval',
#             'pending_shipping',
#             'declined_orders',
#             'completed_orders'
#         ]
#
#         for table in tables:
#             # First drop the table if it exists
#             drop_sql = f"DROP TABLE IF EXISTS {table}"
#             cursor.execute(drop_sql)
#             print(f"Dropped table {table}")
#
#             # Then create the new table structure
#             create_sql = f"""
#             CREATE TABLE {table} (
#                 id INT AUTO_INCREMENT PRIMARY KEY,
#                 cart JSON NOT NULL,
#                 date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#             )
#             """
#             cursor.execute(create_sql)
#             print(f"Created new table {table} with simplified structure")
#
#     # Commit the changes
#     connection.commit()
#     print("All tables have been successfully updated")
#
# except Exception as e:
#     print(f"An error occurred: {e}")
#     connection.rollback()
#
# finally:
#     connection.close()

import pymysql

# اطلاعات اتصال به دیتابیس
db_config = {
    'host': '188.34.178.143',
    'user': 'amirhossein',
    'password': 'g9x76Z!8W]Co1',
    'database': 'modem'
}


with pymysql.connect(**db_config) as conn:
    with conn.cursor() as cursor:
        sql = "UPDATE users SET is_owner = True WHERE full_name = 'امیرحسین سلطانی'"
        cursor.execute(sql)
        conn.commit()

with pymysql.connect(**db_config) as conn:
    with conn.cursor() as cursor:
        sql = "SELECT * FROM users WHERE full_name = 'امیرحسین سلطانی'"
        cursor.execute(sql)
        results = cursor.fetchall()[0][6]
        print(results)



# try:
#     # اتصال به دیتابیس
#     connection = pymysql.connect(**db_config)
#     cursor = connection.cursor()
#
#     # دریافت لیست تمام جداول موجود در دیتابیس
#     cursor.execute("SHOW TABLES")
#     tables = cursor.fetchall()
#
#     if not tables:
#         print("هیچ جدولی در دیتابیس یافت نشد!")
#     else:
#         print("🔹 لیست جداول و ستون‌های دیتابیس:")
#         for table in tables:
#             table_name = table[0]
#             print(f"\n📌 جدول: {table_name}")
#
#             # دریافت اطلاعات ستون‌های هر جدول
#             cursor.execute(f"DESCRIBE {table_name}")
#             columns = cursor.fetchall()
#
#             print("┌───────────────┬───────────────┬───────────────┬───────────────┐")
#             print("│ نام ستون     │ نوع داده      │ Null?         │ Extra         │")
#             print("├───────────────┼───────────────┼───────────────┼───────────────┤")
#
#             for column in columns:
#                 name = column[0]
#                 data_type = column[1]
#                 nullable = "YES" if column[2] == "YES" else "NO"
#                 extra = column[5] if column[5] else "-"
#
#                 print(f"│ {name.ljust(13)} │ {data_type.ljust(13)} │ {nullable.ljust(13)} │ {extra.ljust(13)} │")
#
#             print("└───────────────┴───────────────┴───────────────┴───────────────┘")
#
# except pymysql.Error as e:
#     print(f"❌ خطا در اتصال به دیتابیس: {e}")
#
# finally:
#     if connection:
#         connection.close()

#
# import pymysql
#
# # اطلاعات اتصال به دیتابیس
# db_config = {
#     'host': '188.34.178.143',
#     'user': 'amirhossein',
#     'password': 'g9x76Z!8W]Co1',
#     'database': 'modem',
#     'charset': 'utf8mb4',
#     'cursorclass': pymysql.cursors.DictCursor
# }
#
# try:
#     # اتصال به دیتابیس
#     connection = pymysql.connect(**db_config)
#
#     with connection.cursor() as cursor:
#         # دستور SQL برای حذف تمام رکوردها
#         sql = "DELETE FROM cart_items"
#
#         # اجرای دستور
#         cursor.execute(sql)
#
#         # تعداد رکوردهای حذف شده
#         deleted_rows = cursor.rowcount
#         print(f"تعداد رکوردهای حذف شده: {deleted_rows}")
#
#     # ذخیره تغییرات
#     connection.commit()
#     print("✅ تمام رکوردهای جدول cart_items با موفقیت حذف شدند.")
#
# except pymysql.Error as e:
#     print(f"❌ خطا در حذف رکوردها: {e}")
#     if 'connection' in locals():
#         connection.rollback()
#
# finally:
#     # بستن اتصال
#     if 'connection' in locals() and connection.open:
#         connection.close()
#         print("اتصال به دیتابیس بسته شد.")


# import pymysql
#
# # اطلاعات اتصال
# connection = pymysql.connect(
#     host="188.34.178.143",
#     user="amirhossein",
#     password="g9x76Z!8W]Co1",
#     database="modem"
# )
#
# try:
#     with connection.cursor() as cursor:
#         # بررسی اینکه آیا ستون is_owner وجود دارد یا نه
#         check_column_query = """
#             SELECT COUNT(*)
#             FROM INFORMATION_SCHEMA.COLUMNS
#             WHERE TABLE_SCHEMA = 'modem'
#               AND TABLE_NAME = 'users'
#               AND COLUMN_NAME = 'is_owner';
#         """
#         cursor.execute(check_column_query)
#         result = cursor.fetchone()
#
#         if result[0] == 0:
#             # ستون وجود ندارد، اضافه شود
#             alter_query = """
#                 ALTER TABLE users
#                 ADD COLUMN is_owner BOOLEAN DEFAULT FALSE;
#             """
#             cursor.execute(alter_query)
#             connection.commit()
#             print("ستون is_owner با موفقیت اضافه شد.")
#         else:
#             print("ستون is_owner از قبل وجود دارد.")
# except pymysql.MySQLError as e:
#     print("خطا در اجرای درخواست:", e)
# finally:
#     connection.close()

#
# import pymysql
#
# # اطلاعات اتصال
# connection = pymysql.connect(
#     host="188.34.178.143",
#     user="amirhossein",
#     password="g9x76Z!8W]Co1",
#     database="modem"
# )
#
# try:
#     with connection.cursor() as cursor:
#         update_query = """
#             UPDATE users
#             SET is_owner = TRUE
#             WHERE id = 1;
#         """
#         cursor.execute(update_query)
#         connection.commit()
#         print("کاربر با شناسه 1 به owner تبدیل شد.")
# except pymysql.MySQLError as e:
#     print("خطا در اجرای درخواست:", e)
# finally:
#     connection.close()

