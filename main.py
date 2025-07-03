import logging
from buy_modem_conversation import *
from say_hello import *
from generate_link_admin import *
from add_admin_conversation import *
from add_user_conversation import *
from broadcast_conversation import *
from add_owner_conversation import *
from delete_admin_conversation import *
from pending_approval_conversation import *
from pending_shipping_conversation import *
from edit_card_number_conversation import *
from delete_user_conversation import *
from payment import *
from buy_simcard_conversation import *
from delete_product_conversation import *
from update_user_info import update_user_handler
from dynamic_text_conversation import *
from show_user_info import *
from show_admins import *
from show_users import *
from add_product_conversation import *
from show_products_conversation import *
from update_record_conversation import *
from database import *
from send_completed_orders import *
from send_decline_orders import *
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")




database = Database()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)



# Start Point
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(database.is_owner(update.effective_chat.id))
    if database.is_owner(update.effective_chat.id):
        # Creates owner Panel
        reply_markup = create_owner_panel()
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            reply_markup=reply_markup,
            text="سلام!\nبه پنل مدیریت مالک خوش آمدید."
        )
    elif database.is_admin(update.effective_chat.id):
        # Creates Admin Panel
        reply_markup = create_admin_panel()
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            reply_markup=reply_markup,
            text="سلام!\nبه پنل مدیریت ادمین خوش آمدید."
        )
    else:
        if context.args:

            token = context.args[0]
            if token in available_tokens:

                while token in available_tokens:
                    available_tokens.remove(token)

                if not database.is_contain(update.effective_chat.id, "users", f"chat_id = {update.effective_chat.id}"):
                    user_record = Record(table_name="users", chat_id=update.effective_chat.id)
                    database.add_record(user_record)

        if database.is_contain(update.effective_chat.id, "users", f"chat_id = {update.effective_chat.id}"):
            # Creates User Panel
            reply_markup = create_user_panel()
            text = get_dynamic_text("main", "start", "message")
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                reply_markup=reply_markup,
                text= text
            )



# -------------------------------------------------------------------

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).concurrent_updates(True).build()


    # Canceled For Now:
    # Add User Conversation Handler
    # add_user_conv_handler = add_user_handler()
    # application.add_handler(add_user_conv_handler)

    # dynamic_text_conv_handler
    dynamic_text_conv_handler = dynamic_text_handler()
    application.add_handler(dynamic_text_conv_handler)

    # Edit Card Number
    edit_card_number_conv_handler = edit_card_handler()
    application.add_handler(edit_card_number_conv_handler)


    # Add Product Conversation handler
    add_product_conv_handler = add_product_handler()
    application.add_handler(add_product_conv_handler)

    # Delete Product Conversation Handler
    delete_product_conv_handler = delete_product_handler()
    application.add_handler(delete_product_conv_handler)

    # Update Product Conversation handler
    update_product_conv_handler = update_record_handler()
    application.add_handler(update_product_conv_handler)



    # Buy Conversation
    buy_conv_handler = buy_handler()
    application.add_handler(buy_conv_handler)



    # Modem Conversation handler
    modem_conv_handler = modem_handler()
    application.add_handler(modem_conv_handler)

    # Simcard Conversation handler
    simcard_conv_handler = simcard_handler()
    application.add_handler(simcard_conv_handler)

    # Show User Info handler
    show_user_info_handler = MessageHandler(filters.Regex("^نمایش اطلاعات من$"), show_user_info)
    application.add_handler(show_user_info_handler)

    # Update User Info handler
    update_user_conv_handler = update_user_handler()
    application.add_handler(update_user_conv_handler)

    # send_completed_orders_handler
    send_completed_orders_handler = MessageHandler(filters.Regex("^لیست خرید های تکمیل شده$"), send_completed_orders)
    application.add_handler(send_completed_orders_handler)

    # send_declined_orders_handle
    send_declined_orders_handler = MessageHandler(filters.Regex("^لیست خرید های رد شده$"), send_declined_orders)
    application.add_handler(send_declined_orders_handler)


    # Add Admin Conversation handler
    add_admin_conv_handler = add_admin_handler()
    application.add_handler(add_admin_conv_handler)

    # Add Owner Conversation Handler
    add_owner_conv_handler = add_owner_handler()
    application.add_handler(add_owner_conv_handler)

    # Delete Admin Conversation Handler
    delete_admin_conv_handler = delete_admin_handler()
    application.add_handler(delete_admin_conv_handler)

    # Delete User Conversation
    delete_user_conv_handler = delete_user_handler()
    application.add_handler(delete_user_conv_handler)

    # send broadcast
    broadcast_handler = broadcast_conv_handler()
    application.add_handler(broadcast_handler)

    # Show Product Conversation handler
    show_product_conv_handler = show_product_handler()
    application.add_handler(show_product_conv_handler)

    # Pending Approval Conversation Handler
    pending_approval_conv_handler = pending_approval()
    application.add_handler(pending_approval_conv_handler)

    # Pending Shipping Conversation Handler
    pending_shipping_conv_handler = pending_shipping()
    application.add_handler(pending_shipping_conv_handler)



    # Start Handler
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)



    # Show Admins
    show_admins_handler = MessageHandler(filters.Regex("^نمایش ادمین ها$"), show_admins)
    application.add_handler(show_admins_handler)

    # Generate Token
    generate_link_handler = MessageHandler(filters.Regex("^ساخت لینک عضویت$"), gen_link)
    application.add_handler(generate_link_handler)



    # Show Users Handler
    show_users_handler = MessageHandler(filters.Regex("^نمایش کاربران$"),show_users)
    application.add_handler(show_users_handler)


    # ---------------------------------------------------------------------------------
    # echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    # application.add_handler(echo_handler)

    say_hello_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), say_hello)
    application.add_handler(say_hello_handler)

    # application.add_handler(CallbackQueryHandler(markup_handler))
    # ---------------------------------------------------------------------------------
    application.run_polling()