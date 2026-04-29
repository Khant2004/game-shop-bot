import os

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# =========================================
# SETTINGS
# =========================================

TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = 2007497975

# =========================================
# TEMP STORAGE
# =========================================

user_orders = {}

# =========================================
# START
# =========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [

        [
            InlineKeyboardButton(
                "🔥 Free Fire",
                callback_data="game_ff"
            )
        ],

        [
            InlineKeyboardButton(
                "📱 MLBB",
                callback_data="game_ml"
            )
        ],

        [
            InlineKeyboardButton(
                "📞 Contact Admin",
                callback_data="contact"
            )
        ]

    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        """
🎮 Welcome To Arthur's World

Choose Your Game
""",
        reply_markup=reply_markup
    )


# =========================================
# BUTTON HANDLER
# =========================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    data = query.data

    user_id = query.from_user.id

    # =====================================
    # GAME SELECT
    # =====================================

    if data == "game_ff":

        keyboard = [

            [
                InlineKeyboardButton(
                    "100 Diamond - 1000 Ks",
                    callback_data="ff_100"
                )
            ],

            [
                InlineKeyboardButton(
                    "310 Diamond - 3000 Ks",
                    callback_data="ff_310"
                )
            ],

            [
                InlineKeyboardButton(
                    "520 Diamond - 5000 Ks",
                    callback_data="ff_520"
                )
            ]

        ]

        await query.message.reply_text(
            "🔥 Choose Free Fire Package",
            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )

    elif data == "game_ml":

        keyboard = [

            [
                InlineKeyboardButton(
                    "86 Diamond - 2000 Ks",
                    callback_data="ml_86"
                )
            ],

            [
                InlineKeyboardButton(
                    "172 Diamond - 4000 Ks",
                    callback_data="ml_172"
                )
            ]

        ]

        await query.message.reply_text(
            "📱 Choose MLBB Package",
            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )

    # =====================================
    # PACKAGE SELECT
    # =====================================

    elif data == "ff_100":

        user_orders[user_id] = {

            "game": "Free Fire",
            "package": "100 Diamond",
            "price": "1000 Ks"

        }

        await ask_game_id(
            query,
            "Send Your Free Fire ID"
        )

        context.user_data[
            "waiting_game_id"
        ] = True

    elif data == "ff_310":

        user_orders[user_id] = {

            "game": "Free Fire",
            "package": "310 Diamond",
            "price": "3000 Ks"

        }

        await ask_game_id(
            query,
            "Send Your Free Fire ID"
        )

        context.user_data[
            "waiting_game_id"
        ] = True

    elif data == "ff_520":

        user_orders[user_id] = {

            "game": "Free Fire",
            "package": "520 Diamond",
            "price": "5000 Ks"

        }

        await ask_game_id(
            query,
            "Send Your Free Fire ID"
        )

        context.user_data[
            "waiting_game_id"
        ] = True

    elif data == "ml_86":

        user_orders[user_id] = {

            "game": "MLBB",
            "package": "86 Diamond",
            "price": "2000 Ks"

        }

        await ask_game_id(
            query,
            "Send Your MLBB ID"
        )

        context.user_data[
            "waiting_game_id"
        ] = True

    elif data == "ml_172":

        user_orders[user_id] = {

            "game": "MLBB",
            "package": "172 Diamond",
            "price": "4000 Ks"

        }

        await ask_game_id(
            query,
            "Send Your MLBB ID"
        )

        context.user_data[
            "waiting_game_id"
        ] = True

    # =====================================
    # ORDER CONFIRM
    # =====================================

    elif data == "confirm_order":

        keyboard = [

            [
                InlineKeyboardButton(
                    "💸 Continue Payment",
                    callback_data="payment"
                )
            ],

            [
                InlineKeyboardButton(
                    "❌ Cancel",
                    callback_data="cancel"
                )
            ]

        ]

        await query.message.reply_text(
            """
✅ Order Confirmed

Press Continue Payment
""",
            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )

    # =====================================
    # PAYMENT
    # =====================================

    elif data == "payment":

        context.user_data[
            "waiting_payment"
        ] = True

        await query.message.reply_text(
            """
💸 Payment Info

WavePay - 09xxxxxxxxx

📸 Send Payment Screenshot
"""
        )

    # =====================================
    # CANCEL
    # =====================================

    elif data == "cancel":

        await query.message.reply_text(
            "❌ Order Cancelled"
        )

    # =====================================
    # ADMIN CONFIRM
    # =====================================

    elif data.startswith("admin_confirm_"):

        customer_id = int(
            data.replace(
                "admin_confirm_",
                ""
            )
        )

        keyboard = [

            [
                InlineKeyboardButton(
                    "📦 Delivered",
                    callback_data=f"""
deliver_{customer_id}
"""
                )
            ]

        ]

        await context.bot.send_message(
            chat_id=customer_id,

            text="""
✅ PAYMENT CONFIRMED

⏳ Your Order Is Processing
"""
        )

        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )

    # =====================================
    # DELIVER
    # =====================================

    elif data.startswith("deliver_"):

        customer_id = int(
            data.replace(
                "deliver_",
                ""
            )
        )

        await context.bot.send_message(
            chat_id=customer_id,

            text="""
🎉 ORDER COMPLETED

✅ Topup Delivered

❤️ Thank You
"""
        )

        await query.edit_message_reply_markup(
            reply_markup=None
        )


# =========================================
# ASK GAME ID
# =========================================

async def ask_game_id(
    query,
    text
):

    await query.message.reply_text(
        f"""
🆔 {text}
"""
    )


# =========================================
# MESSAGE HANDLER
# =========================================

async def message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.message.from_user.id

    # =====================================
    # GAME ID
    # =====================================

    if context.user_data.get(
        "waiting_game_id"
    ):

        game_id = update.message.text

        user_orders[user_id][
            "game_id"
        ] = game_id

        context.user_data[
            "waiting_game_id"
        ] = False

        keyboard = [

            [
                InlineKeyboardButton(
                    "✅ Confirm Order",
                    callback_data="confirm_order"
                )
            ],

            [
                InlineKeyboardButton(
                    "❌ Cancel",
                    callback_data="cancel"
                )
            ]

        ]

        order = user_orders[user_id]

        text = f"""
🛒 ORDER SUMMARY

🎮 Game:
{order['game']}

💎 Package:
{order['package']}

💰 Price:
{order['price']}

🆔 Game ID:
{game_id}

Confirm Order?
"""

        await update.message.reply_text(
            text,

            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )

        return


# =========================================
# PHOTO HANDLER
# =========================================

async def photo_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.message.from_user.id

    if not context.user_data.get(
        "waiting_payment"
    ):
        return

    order = user_orders[user_id]

    user = update.message.from_user

    username = user.username

    if username:

        username_text = f"""
@{username}
"""

    else:

        username_text = "No Username"

    caption = f"""
🛒 NEW ORDER

👤 Username:
{username_text}

🆔 Telegram ID:
{user.id}

🎮 Game:
{order['game']}

💎 Package:
{order['package']}

💰 Price:
{order['price']}

🎯 Game ID:
{order['game_id']}
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "✅ Confirm Payment",

                callback_data=f"""
admin_confirm_{user.id}
"""
            )
        ]

    ]

    photo = update.message.photo[-1].file_id

    await context.bot.send_photo(

        chat_id=ADMIN_ID,

        photo=photo,

        caption=caption,

        reply_markup=InlineKeyboardMarkup(
            keyboard
        )

    )

    await update.message.reply_text(
        """
✅ Screenshot Received

⏳ Waiting Admin Confirm
"""
    )

    context.user_data[
        "waiting_payment"
    ] = False


# =========================================
# MAIN
# =========================================

def main():

    app = Application.builder().token(
        TOKEN
    ).build()

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT &
            ~filters.COMMAND,

            message_handler
        )
    )

    app.add_handler(
        MessageHandler(
            filters.PHOTO,

            photo_handler
        )
    )

    print(
        "✅ BOT RUNNING..."
    )

    app.run_polling()


# =========================================
# RUN
# =========================================

if __name__ == "__main__":

    main()
