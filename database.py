import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")



PANEL_BOT_TOKEN = os.getenv("PANEL_BOT_TOKEN")
GROUP_BOT_TOKEN = os.getenv('GROUP_BOT_TOKEN')

class Record:
    def __init__(self, table_name: str,
                 username=None,
                 chat_id = None,
                 is_owner = None,
                 is_admin = None,
                 phone = None,
                 address = None,
                 product_model=None,
                 product_name=None,
                 is_new=None,
                 product_price=None,
                 product_count=None,
                 file_id="0",
                 product_id=None,
                 total_price=None,
                 card_number=None,
                 product_description=None,
                 cart=None,
                 product_table = None
                 ):
        # Database Info
        self.host = DB_HOST
        self.user = DB_USER
        self.password = DB_PASSWORD
        self.database = DB_NAME

        # Data Info
        self.table_name = table_name
        self.users = None
        self.modem = None
        self.simcard = None
        self.pending_shipping = None
        self.pending_approval = None
        self.declined_orders = None
        self.completed_orders = None
        self.cart_items = None

        self.cart = cart
        self.product_table = product_table

        # modem and simcard (Note that most of them are used in other Tables)
        self.product_model = product_model
        self.product_name = product_name
        self.product_price = product_price
        self.product_count = product_count
        self.product_description = product_description
        self.is_new = is_new
        self.file_id = file_id

        # users
        self.username = username
        self.chat_id = chat_id
        self.is_admin = is_admin
        self.phone = phone
        self.address = address
        self.is_owner = is_owner

        # other properties needed for other tables
        self.product_id = product_id
        self.card_number = card_number
        self.total_price = total_price

        # user info dict
        if self.table_name == "users":
            self.users = {
                "chat_id": self.chat_id,
                "full_name": self.username,
                "is_admin": self.is_admin,
                "phone_number": self.phone,
                "address": self.address,
                "is_owner": self.is_owner,
            }

        # modem info dict
        elif self.table_name == "modem":
            self.modem = {
                "model": self.product_model,
                "name": self.product_name,
                "is_new": self.is_new,
                "price": self.product_price,
                "count": self.product_count,
                "image_id": self.file_id,
                "description": self.product_description
            }


        # simcard info dict
        elif self.table_name == "simcard":
            self.simcard = {
                "model": self.product_model,
                "name": self.product_name,
                "description": self.product_description,
                "count": self.product_count,
                "price": self.product_price,
            }


        # pending_approval info dict
        elif self.table_name == "pending_approval":
            self.pending_approval = {
                "cart": self.cart,
            }


        # pending_shipping info dict
        elif self.table_name == "pending_shipping":
            self.pending_shipping = {
                "cart": self.cart,
            }


        # declined_orders info dict
        elif self.table_name == "declined_orders":
            self.declined_orders = {
                "cart": self.cart,
            }


        # completed_orders info dict
        elif self.table_name == "completed_orders":
            self.completed_orders = {
                "cart": self.cart,
            }


        # cart_items info dict
        elif self.table_name == "cart_items":
            self.cart_items = {
                "product_table": self.product_table,
                "product_id": self.product_id,
                "count": self.product_count,
                "chat_id": self.chat_id
            }





class Database:
    def __init__(self):
        self.host = "188.34.178.143"
        self.user = "amirhossein"
        self.password = "g9x76Z!8W]Co1"
        self.database = "modem"


    def add_record(self, record: Record):
        sql = None
        values = None
        try:
            with pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database) as conn:
                with conn.cursor() as cursor:
                    if record.table_name == "users":
                        sql = 'INSERT INTO users (full_name, chat_id, phone_number, is_admin, address, is_owner) VALUES (%s, %s, %s, %s, %s, %s)'
                        values = (record.username, record.chat_id, record.phone, record.is_admin, record.address, record.is_owner)
                    elif record.table_name == "modem":
                        sql = 'INSERT INTO modem (model, name, is_new, price, count, image_id, description) VALUES (%s, %s, %s, %s, %s, %s, %s)'
                        values = (record.product_model, record.product_name, record.is_new, record.product_price, record.product_count, record.file_id, record.product_description)
                    elif record.table_name == "simcard":
                        sql = 'INSERT INTO simcard (model, name, price, count, description) VALUES (%s, %s, %s, %s, %s)'
                        values = (record.product_model, record.product_name, record.product_price, record.product_count, record.product_description)
                    elif record.table_name == "pending_approval":
                        sql = 'INSERT INTO pending_approval (cart) VALUES (%s)'
                        values = (record.cart)
                    elif record.table_name == "pending_shipping":
                        sql = 'INSERT INTO pending_shipping (cart) VALUES (%s)'
                        values = (record.cart)
                    elif record.table_name == "declined_orders":
                        sql = 'INSERT INTO declined_orders (cart) VALUES (%s)'
                        values = (record.cart)
                    elif record.table_name == "completed_orders":
                        sql = 'INSERT INTO completed_orders (cart) VALUES (%s)'
                        values = (record.cart)
                    elif record.table_name == "cart_items":
                        sql = 'INSERT INTO cart_items (product_table, product_id, count, chat_id) VALUES (%s, %s, %s, %s)'
                        values = (record.product_table, record.product_id, record.product_count, record.chat_id)

                    if sql and values:
                        cursor.execute(sql, values)
                        conn.commit()
                        return True
                    else:
                        print("Data did not added")
                        return False
        except Exception as e:
            print(e)
            return False


    def fetch_data(self,table_name, condition:str=None):
        try:
            with pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database) as conn:
                with conn.cursor() as cursor:
                    query = f"SELECT * FROM {table_name}"

                    if condition:
                        query += f" WHERE {condition}"


                    cursor.execute(query)
                    rows = cursor.fetchall()

            # check if there are some result or not
            if not rows:
                text = f"No records found in table '{table_name}'."
                print(text)
                return False
            else:
                print(rows)
                return rows

        except Exception as e:
            print(e)
            return False


    def is_contain(self, value, table_name, condition:str=None):
        rows = self.fetch_data(table_name, condition)
        if rows:
            for row in rows:
                if value in row:
                    return True
        return False



    def is_admin(self, chat_id):
        try:
            with pymysql.connect(host=self.host, user=self.user, password=self.password,
                                 database=self.database) as conn:
                with conn.cursor() as cursor:
                    sql = "SELECT is_admin FROM users WHERE chat_id = %s"
                    cursor.execute(sql, (chat_id,))
                    result = cursor.fetchone()

                    if result and result[0] == 1:
                        return True
                    return False
        except Exception as e:
            print(e)
            return False


    def is_owner(self, chat_id):
        try:
            with pymysql.connect(host=self.host, user=self.user, password=self.password,
                                 database=self.database) as conn:
                with conn.cursor() as cursor:
                    sql = "SELECT is_owner FROM users WHERE chat_id = %s"
                    cursor.execute(sql, (chat_id,))
                    result = cursor.fetchone()

                    if result and result[0] == 1:
                        return True
                    return False
        except Exception as e:
            print(e)
            return False



    def delete_record(self, table_name, condition:str):
        query = f"DELETE FROM {table_name} WHERE {condition}"

        try:
            with pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    conn.commit()
                    print(f"✅ Record(s) deleted from '{table_name}' successfully!")
                    return True
        except Exception as e:
            print(e)
            return False

    def update_record(self, record: Record,  condition:str):
        updates = {}

        if record.table_name == "users":
            updates = record.users
        elif record.table_name == "modem":
            updates = record.modem
        elif record.table_name == "simcard":
            updates = record.simcard
        elif record.table_name == "pending_approval":
            updates = record.pending_approval
        elif record.table_name == "pending_shipping":
            updates = record.pending_shipping
        elif record.table_name == "declined_orders":
            updates = record.declined_orders
        elif record.table_name == "completed_orders":
            updates = record.completed_orders
        elif record.table_name == "cart_items":
            updates = record.cart_items

        set_clause = ", ".join([f"{column} = %s" for column in updates.keys() if updates[column] is not None])
        values = [value for value in updates.values() if value is not None]

        query = f"UPDATE {record.table_name} SET {set_clause}"

        query += f" WHERE {condition}"
        print("Final update query:", query)
        print("Values:", values)

        try:
            with pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, values)
                    conn.commit()
                    print("✅ Record updated successfully!")
                    return True
        except Exception as e:
            print(e)
            return False












