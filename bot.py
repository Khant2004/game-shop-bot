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
# USER DATA
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
        "🎮 Welcome To EngageX Hub\n\nChoose Game:",
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
    # FREE FIRE
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

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "🔥 Choose Free Fire Package",
            reply_markup=reply_markup
        )

    # =====================================
    # MLBB
    # =====================================

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

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "📱 Choose MLBB Package",
            reply_markup=reply_markup
        )

    # =====================================
    # CONTACT
    # =====================================

    elif data == "contact":

        await query.message.reply_text(
            "📞 Admin Username:\n@ar_thur21"
        )

    # =====================================
    # FREE FIRE PACKAGES
    # =====================================

    elif data == "ff_100":

        user_orders[user_id] = {
            "game": "Free Fire",
            "package": "100 Diamond",
            "price": "1000 Ks"
        }

        await query.message.reply_text(
            "🆔 Send Your Free Fire ID"
        )

        context.user_data["waiting_id"] = True

    elif data == "ff_310":

        user_orders[user_id] = {
            "game": "Free Fire",
            "package": "310 Diamond",
            "price": "3000 Ks"
        }

        await query.message.reply_text(
            "🆔 Send Your Free Fire ID"
        )

        context.user_data["waiting_id"] = True

    elif data == "ff_520":

        user_orders[user_id] = {
            "game": "Free Fire",
            "package": "520 Diamond",
            "price": "5000 Ks"
        }

        await query.message.reply_text(
            "🆔 Send Your Free Fire ID"
        )

        context.user_data["waiting_id"] = True

    # =====================================
    # MLBB PACKAGES
    # =====================================

    elif data == "ml_86":

        user_orders[user_id] = {
            "game": "MLBB",
            "package": "86 Diamond",
            "price": "2000 Ks"
        }

        await query.message.reply_text(
            "🆔 Send Your MLBB ID"
        )

        context.user_data["waiting_id"] = True

    elif data == "ml_172":

        user_orders[user_id] = {
            "game": "MLBB",
            "package": "172 Diamond",
            "price": "4000 Ks"
        }

        await query.message.reply_text(
            "🆔 Send Your MLBB ID"
        )

        context.user_data["waiting_id"] = True

    # =====================================
    # CONFIRM ORDER
    # =====================================

    elif data.startswith("confirm_"):

        customer_id = int(
            data.split("_")[1]
        )

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "📦 Delivered",
                    callback_data=f"deliver_{customer_id}"
                )
            ]

        ])

        await context.bot.send_message(
            chat_id=customer_id,
            text="""
✅ PAYMENT CONFIRMED

⏳ Your order is processing.
"""
        )

        await query.edit_message_reply_markup(
            reply_markup=keyboard
        )

    # =====================================
    # DELIVER ORDER
    # =====================================

    elif data.startswith("deliver_"):

        customer_id = int(
            data.split("_")[1]
        )

        await context.bot.send_message(
            chat_id=customer_id,
            text="""
🎉 ORDER COMPLETED

✅ Your topup has been delivered.

❤️ Thank you for buying.
"""
        )

        await query.edit_message_reply_markup(
            reply_markup=None
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

    if context.user_data.get("waiting_id"):

        game_id = update.message.text

        user_orders[user_id]["game_id"] = game_id

        context.user_data["waiting_id"] = False

        context.user_data["waiting_payment"] = True

        await update.message.reply_text(
            """
💰 PAYMENT INFO

WavePay - 09xxxxxxxxx

📸 Send Payment Screenshot
"""
        )

        return

    # =====================================
    # WAIT PAYMENT
    # =====================================

    if context.user_data.get("waiting_payment"):

        await update.message.reply_text(
            "📸 Please send payment screenshot image."
        )


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
        username_text = f"@{username}"
    else:
        username_text = "No Username"

    caption = f"""
🛒 NEW ORDER

👤 Username: {username_text}

🆔 Telegram ID: {user.id}

🎮 Game: {order['game']}

💎 Package: {order['package']}

💰 Price: {order['price']}

🎯 Game ID: {order['game_id']}
"""

    keyboard = InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "✅ Confirm",
                callback_data=f"confirm_{user.id}"
            )
        ]

    ])

    photo = update.message.photo[-1].file_id

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo,
        caption=caption,
        reply_markup=keyboard
    )

    await update.message.reply_text(
        """
✅ Screenshot Received

⏳ Waiting Admin Confirm
"""
    )

    context.user_data["waiting_payment"] = False


# =========================================
# MAIN
# =========================================

def main():

    app = Application.builder().token(
        TOKEN
    ).build()

    app.add_handler(
        CommandHandler("start", start)
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

    print("✅ BOT RUNNING...")

    app.run_polling()


# =========================================
# RUN
# =========================================

if __name__ == "__main__":
    main()
