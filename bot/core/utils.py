from pyexpat.errors import messages
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import re
import json
from bot.core.database import Database








def create_user_break_button():
    keyboard = [
        ["لغو عملیات!"],
        ["خرید سیمکارت", "خرید مودم"],
        ["نمایش اطلاعات من", "ویرایش اطلاعات من"],
        ["نمایش سبد خرید"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard,resize_keyboard=True)
    return reply_markup

def create_break_button():
    keyboard = [
        ["لغو عملیات!"],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard,resize_keyboard=True)
    return reply_markup



async def user_panel_break_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = create_user_panel()
    context.user_data.clear()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="عملیات لغو شد!", reply_markup=reply_markup)
    return ConversationHandler.END

# ------------------------------
# # active one conversation per moment
#     if context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
#             "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
#             "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
#             "show_product") or context.user_data.get("update_record") or context.user_data.get(
#             'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
#             'delete_user') or context.user_data.get('add_owner'):
#         return ConversationHandler.END
# ------------------------------

#     if database.is_owner(update.effective_chat.id):
#         reply_markup = create_owner_panel()
#     elif database.is_admin(update.effective_chat.id):
#         reply_markup = create_admin_panel()

async def admin_owner_panel_break_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    database = Database()
    if database.is_owner(update.effective_chat.id):
        reply_markup = create_owner_panel()
    elif database.is_admin(update.effective_chat.id):
        reply_markup = create_admin_panel()
    context.user_data.clear()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="عملیات لغو شد!",reply_markup=reply_markup)
    return ConversationHandler.END

async def owner_panel_break_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = create_owner_panel()
    context.user_data.clear()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="عملیات لغو شد!",reply_markup=reply_markup)
    return ConversationHandler.END

async def break_conversation(update:Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="عملیات قبلی لغو شد!")
    return ConversationHandler.END


def create_user_panel():
    keyboards = [
        ["خرید سیمکارت", "خرید مودم"],
        ["نمایش اطلاعات من","ویرایش اطلاعات من"],
        ["نمایش سبد خرید"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard=keyboards, one_time_keyboard=True, resize_keyboard=True)
    return reply_markup


def create_admin_panel():
    keyboards = [
        ["نمایش اطلاعات من","ویرایش اطلاعات من"],
        ["حذف محصول", "اضافه کردن محصول"],
        ["ویرایش محصول", "نمایش محصولات"],
        ["نمایش ادمین ها", "نمایش کاربران"],
        ["تغییر محتوای نوشته ها","ارسال پیام گروهی"],
        ["ساخت لینک عضویت","حذف کاربر"],
        ["لیست سفارش های در انتظار تایید"],
        ["لیست سفارش های در انتظار ارسال"],
        ["لیست خرید های تکمیل شده"],
        ["لیست خرید های رد شده"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard=keyboards, one_time_keyboard=True, resize_keyboard=True)

    return reply_markup

    # # active one conversation per moment
    # if context.user_data.get("add_product") or context.user_data.get("delete_admin") or
    # context.user_data.get(
    #         "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
    #     "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
    #     "show_product"):
    #     return ConversationHandler.END

# # active one conversation per moment
#     if context.user_data.get("add_product") or context.user_data.get("delete_admin") or
#     context.user_data.get("delete_product") or context.user_data.get("dynamic_text") or
#     context.user_data.get("pending_approval") or context.user_data.get("pending_shipping") or
#     context.user_data.get("show_product") or
#     context.user_data.get("update_record") or context.user_data.get('update_user_info_conv') or
#     context.user_data.get('add_admin') or context.user_data.get('delete_user') or
#     context.user_data.get('add_owner') or :
#         return ConversationHandler.END


# context.user_data.get('update_user_info_conv')

# context.user_data.get('add_admin')
# context.user_data.get('delete_user')
# context.user_data.get('add_owner')

# ------------------------------
# # active one conversation per moment
#     if context.user_data.get("add_product") or context.user_data.get("delete_admin") or context.user_data.get(
#             "delete_product") or context.user_data.get("dynamic_text") or context.user_data.get(
#             "pending_approval") or context.user_data.get("pending_shipping") or context.user_data.get(
#             "show_product") or context.user_data.get("update_record") or context.user_data.get(
#             'update_user_info_conv') or context.user_data.get('add_admin') or context.user_data.get(
#             'delete_user') or context.user_data.get('add_owner'):
#         return ConversationHandler.END
# ------------------------------

def create_owner_panel():
    keyboards = [
        ["نمایش اطلاعات من","ویرایش اطلاعات من"],
        ["حذف محصول", "اضافه کردن محصول"],
        ["حذف ادمین", "اضافه کردن ادمین"],
        ["ویرایش محصول", "نمایش محصولات"],
        ["نمایش ادمین ها", "نمایش کاربران"],
        ["تغییر محتوای نوشته ها","ارسال پیام گروهی"],
        ["ساخت لینک عضویت","حذف کاربر"],
        ["لیست سفارش های در انتظار تایید"],
        ["لیست سفارش های در انتظار ارسال"],
        ["لیست خرید های تکمیل شده"],
        ["لیست خرید های رد شده"],
        ["ویرایش شماره کارت"],
        ["ارتقا ادمین به مالک"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard=keyboards, one_time_keyboard=True, resize_keyboard=True)

    return reply_markup


# Generate Text for admin
def show_admin_admins_users(admin_or_user):
    show = ""
    for adser in admin_or_user:
        show += f"{adser[2]}->\nid : {adser[0]}\nphone number: {adser[4]}\nchat id: {adser[1]}\n"
        show += "\n\n"
    return show

def show_admin_simcards(simcards):
    show = ""
    for sim in simcards:
        show += f"{sim[2]}->\nid : {sim[0]}\nmodel : {sim[1]}\nprice : {sim[5]}\ncount : {sim[4]}\ndescription : {sim[3]}"
        show += "\n\n"
    return show

def show_admin_modems(modems):
    show = ""
    for modem in modems:
        if int(modem[3]) == 1:
            situation = "new"
        else:
            situation = "pre-owned"

        show += f"{modem[2]}->\nid : {modem[0]}\nmodel : {modem[1]}\nsituation : {situation}\nprice : {modem[4]}\ncount : {modem[5]}\nimage id : {modem[6]}\ndescription : {modem[7]}"
        show += "\n\n"
    return show












# Data Format Checkers
def convert_numbers(text):
    fa_to_en = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
    return text.translate(fa_to_en)


def is_valid_number(value):
    return value.isdigit() and int(value) > 0


def is_valid_name(value):
    return bool(re.match(r'^[\u0600-\u06FFa-zA-Z\s]+$', value))


def is_valid_phone(value):
    return bool(re.match(r'^09\d{9}$', value))


def is_valid_address(value):
    return len(value.strip()) >= 10






DYNAMIC_TEXT_DEFAULTS = {
    "main": {
        "start":{
            "message": {
                "text": "به ربات فروش مودم و سیمکارت ارتباطات نوین خوش آمدید\n\nدرصورتی که سوال و یا احتیاج به راهنمایی داشتید، می توانید از طریق پشتیبانی ما را درجریان مشکل خود قرار بدهید:\n@ID_Test",
                "vars": []
            }
        }
    },
    "show_user_info":{
        "show_user_info":{
            "message":{
                "text":"""نام و نام خانوادگی: {full_name}
    شماره تماس:              {phone}
    آدرس:              {address}""",
                "vars": ["{address}","{phone}","{address}"]

            }
        }
    },
    "modem":{
        "modem_situation_options_buy": {
            "message": {
                "text": "لطفا یکی از گزینه های زیر را انتخاب کنید.",
                "vars": []
            },
            "option_pre-owned": {
                "text": "خرید مودم استوک",
                "vars": []
            },
            "option_new": {
                "text": "خرید مودم آکبند",
                "vars": []
            },
            "no_inventory":{
                "text": "خرید مودم آکبند",
                "vars": []
            },
        },
        "modem_model_options_buy": {
            "message": {
                "text": "با توجه به توضیحات گفته شده، لطفا گزینه مناسب خود را انتخاب کنید.\nمودم ها برای تصمیم گیری بهتر شما دارای عکس هستند.\n\n1. مودم 5G: این مودم با بهره‌گیری از نسل پنجم اینترنت، بالاترین سرعت دانلود و آپلود، تأخیر بسیار کم و عملکردی فوق‌العاده را برای استریم، بازی‌های آنلاین، هوش مصنوعی و ارتباطات پیشرفته ارائه می‌دهد.\n\n3. با بهره‌گیری از فناوری اینترنت ثابت TD-LTE، این مودم اتصال پایدار، سرعت بالا و پهنای باند وسیع را بدون نیاز به خط تلفن ارائه می‌دهد و برای مصارف خانگی، سازمانی و کسب‌وکارها گزینه‌ای مطمئن محسوب می‌شود.\n\n4. این مودم با پشتیبانی از اینترنت همراه پرسرعت و پوشش سراسری، گزینه‌ای ایده‌آل برای استفاده روزمره، تماشای آنلاین محتوا، انجام کارهای اداری و ارتباطات بی‌وقفه در هر مکان است.\n",
                "vars": []
            },
            "model_options": {
                "text": "مودم {model}",
                "vars": ["{model}"]
            },
            "return_option": {
                "text": "بازگشت",
                "vars": []
            },

        },
        "modem_name_options_buy": {
            "message": {
            "text": "لطفا مودم دلخواه خودتان را انتخاب کنید.",
             "vars": []
            },
            "name_options": {
                "text": "{modem_name}",
                "vars": ["{modem_name}"]
            },
            "return_option": {
                "text": "بازگشت",
                "vars": []
            },
        },

        "modem_description_buy":{
            "message": {
                "text": "متن تستی {description}",
                "vars": ["{description}", "{name}", "{model}", "{price}", "{inventory}", "{situation}"]
            },
            "buy_option": {
                "text": "خرید {name}",
                "vars": ["{description}", "{name}", "{model}", "{price}", "{inventory}", "{situation}"]
            },
            "return_option": {
                "text": "بازگشت",
                "vars": []
            },
        },

        "modem_count_buy": {
            "message":{
                "text": "لطفا تعداد سفارش خود را وارد کنید:",
                "vars": []
            }

        },
        "store_modem_buy": {
            "message":{
                "text": "مودم با موفقیت در سبد محصولات ذخیره شد.",
                "vars": []
            },
            "invalid_number":{
                "text": "❌ مقدار نامعتبر است! لطفا یک عدد معتبر وارد کنید:",
                "vars": []
            },
            "no_inventory": {
                "text": "متاسفانه از این کالا به تعداد {inventory} موجود می باشد. لطفا مقدار کمتری وارد کنید:",
                "vars": ["{inventory}", "{name}", "{user_input}"]
            },

        }
    },

    "simcard":{
        "simcard_model_options_buy":{
            "message":{
                "text": "با توجه به توضیحات زیر، لطفا نوع سیم‌کارت مناسب مودم خود را انتخاب کنید.\n\n1. سیم‌کارت 5G: این سیم‌کارت مخصوص مودم‌های 5G بوده و بالاترین سرعت اینترنت نسل پنجم را ارائه می‌دهد. مناسب برای مودم‌های پیشرفته جهت استریم، بازی آنلاین، دانلودهای حجیم و استفاده در کسب‌وکارهایی که نیاز به اینترنت پایدار و پرسرعت دارند.\n\n2. سیم‌کارت TD-LTE: این سیم‌کارت ویژه مودم‌های TD-LTE طراحی شده و اینترنت ثابت و پرسرعت را بدون نیاز به خط تلفن فراهم می‌کند. گزینه‌ای مناسب برای استفاده خانگی و سازمانی با مصرف بالا و نیاز به پایداری.\n\n3. سیم‌کارت 4G: این سیم‌کارت مناسب مودم‌های 4G و دستگاه‌های اینترنت همراه است. سرعت مناسب، پوشش سراسری و قیمت اقتصادی، انتخابی خوب برای استفاده روزمره، کارهای اداری و اتصال در سفر.",
                "vars": []
            },
            "model_options":{
                "text": "سیمکارت {model}",
                "vars": ["{model}"]
            }
        },
        "simcard_name_options_buy": {
            "message":{
                "text": "لطفا سیمکارت دلخواه خودتان را انتخاب کنید.",
                "vars": []
            },
            "name_options":{
                "text": "{simcard_name}",
                "vars": ["{simcard_name}"]
            }
        },
        "simcard_description_buy":{
            "message": {
                "text": "متن تستی {description}",
                "vars": ["{description}", "{name}", "{model}", "{price}", "{inventory}"]
            },
            "buy_option": {
                "text": "خرید {name}",
                "vars": ["{description}", "{name}", "{model}", "{price}", "{inventory}", "{situation}"]
            },
            "return_option": {
                "text": "بازگشت",
                "vars": []
            },
        },
        "simcard_count_buy":{
            "message":{
                "text": "لطفا تعداد سفارش خود را وارد کنید:",
                "vars": []
            }
        },
        "store_simcard_buy":{
            "message": {
                "text": "سیمکارت با موفقیت در سبد محصولات ذخیره شد.",
                "vars": []
            },
            "invalid_number": {
                "text": "❌ مقدار نامعتبر است! لطفا یک عدد معتبر وارد کنید:",
                "vars": []
            },
            "no_inventory": {
                "text": "متاسفانه از این کالا به تعداد {inventory} موجود می باشد. لطفا مقدار کمتری وارد کنید:",
                "vars": ["{inventory}", "{name}", "{user_input}"]
            },
        }
    },

    "payment":{
        "payment":{
            "order_head": {
                "text": "",
                "vars": []
            },
            "order_template_modem": {
                "text": (
                "🔢 {counter}- {product_name}\n"
                "🆔 شماره سفارش: {order_id}\n"
                "🏷️ وضعیت: {product_situation}\n"
                "📊 تعداد سفارش: {order_count}\n"
                "💰 قیمت فروشگاه: {price} تومان\n"
                "💳 قابل پرداخت: {order_total_price} تومان\n\n"
                ),
                "vars": ["{counter}","{product_name}","{order_id}","{order_count}", "{price}","{order_total_price}", "{product_situation}"]
            },
            "order_template_simcard": {
                "text": (
                "🔢 {counter}- {product_name}\n"
                "🆔 شماره سفارش: {order_id}\n"
                "📊 تعداد سفارش: {order_count}\n"
                "💰 قیمت فروشگاه: {price} تومان\n"
                "💳 قابل پرداخت: {order_total_price} تومان\n\n"
                ),
                "vars": ["{counter}","{product_name}","{order_id}","{order_count}", "{price}","{order_total_price}"]
            },
            "order_footer": {
                "text": "",
                "vars": ["{total_price}"]
            },
            "no_cart":{
                "text": "سبد خرید شما خالی می باشد!",
                "vars": []
            },
            "pay_option": {
                "text": "تکمیل خرید",
                "vars": []
            },
            "delete_option": {
                "text": "حذف سفارش",
                "vars": []
            },
            "edit_option": {
                "text": "ویرایش سفارش",
                "vars": []
            },

        },

        "get_id_payment":{
            "message":{
                "text": "لطفا شماره سفارش خود را وارد کنید:",
                "vars": []
            },
        },

        "edit_order_payment": {
            "message":{
                "text": "لطفا تعداد سفارش خود را وارد کنید:",
                "vars": []
            },
            "invalid_user_input": {
                "text": "❌ مقدار نامعتبر است! لطفا یک عدد معتبر وارد کنید:",
                "vars": []
            },
            "invalid_order_id": {
                "text": "❌ مقدار نامعتبر است! لطفا شماره سفارش معتبر وارد کنید:",
                "vars": []
            }
        },

        "edit_count_payment":{
            "success_message":{
                "text": "عملیات با موفقیت انجام شد!",
                "vars": []
            },
            "failed_message":{
                "text": "عملیات انجام نشد!",
                "vars": []
            }
        },

        "delete_order_payment":{
            "success_message":{
                "text": "عملیات با موفقیت انجام شد!",
                "vars": []
            },
            "failed_message": {
                "text": "عملیات انجام نشد!",
                "vars": []
            }
        },

        "review_payment":{
            "message": {
                "text":(
                    "📌 مشخصات سفارشات شما:\n"
                    "{order_text}"
                    "📌 مشخصات گیرنده:\n"
                    "👤 نام و نام خانوادگی: {full_name}\n"
                    "📞 شماره تماس: {phone}\n"
                    "📍 آدرس: {address}\n"
                    "\n"
                    "💰 مبلغ قابل پرداخت: {total_price} تومان\n"
                    "💳 لطفا مبلغ را به شماره کارت زیر واریز کنید و رسید آن را ارسال کنید:\n"
                    "💳 {card_number}"
                ),
                "vars": ["{order_text}", "{full_name}", "{phone}", "{address}", "{total_price}", "{card_number}"]
            }

        }
    },


    "update_user_info":{

    }
}

# additional_data = {"{model}": model}
# get_dynamic_text("modem", "modem_model_options_buy", "model_options", additional_data=additional_data)

# Create File if it doesn't exist
def get_dynamic_text(bunch, function_name, key, additional_data=None):
    """This function returns a dynamic text from a json file. if the file doesn't exist it will create one."""
    try:
        with open("dynamic_text.json","r", encoding="utf-8") as t_file:
            content = json.load(t_file)
    except FileNotFoundError:
        with open("dynamic_text.json", "w", encoding="utf-8") as t_file:
            json.dump(DYNAMIC_TEXT_DEFAULTS, t_file, ensure_ascii=False, indent=4)
        content = DYNAMIC_TEXT_DEFAULTS
    finally:
        text = content[bunch][function_name][key]["text"]
        vars = content[bunch][function_name][key]["vars"]
        if additional_data:
            for var in vars:
                text = text.replace(var, str(additional_data.get(var)))

        return text






