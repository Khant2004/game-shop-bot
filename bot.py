from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# =====================================
# BOT SETTINGS
# =====================================

import os

TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = 2007497975

# =====================================
# GAME DATA
# =====================================

games = {

    "🔥 Free Fire": {
        "100 Diamond": "1000 Ks",
        "310 Diamond": "3000 Ks",
        "520 Diamond": "5000 Ks"
    },

    "⚽ eFootball": {
        "100 Coins": "2000 Ks",
        "500 Coins": "8000 Ks"
    },

    "🔫 PUBG Mobile": {
        "60 UC": "1500 Ks",
        "325 UC": "7000 Ks"
    }
}

# =====================================
# START
# =====================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["🎮 Buy Game"],
        ["📞 Contact"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "🎮 Welcome To EngageX Hub\n\nChoose Option:",
        reply_markup=reply_markup
    )


# =====================================
# HANDLE MESSAGE
# =====================================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    # =================================
    # BUY GAME
    # =================================

    if text == "🎮 Buy Game":

        keyboard = []

        for game in games.keys():
            keyboard.append([game])

        keyboard.append(["❌ Cancel"])

        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )

        await update.message.reply_text(
            "🎮 Choose Game:",
            reply_markup=reply_markup
        )

        return

    # =================================
    # CONTACT
    # =================================

    elif text == "📞 Contact":

        await update.message.reply_text(
            "📞 Admin Contact:\n@ar_thur21"
        )

        return

    # =================================
    # CANCEL
    # =================================

    elif text == "❌ Cancel":

        await start(update, context)
        return

    # =================================
    # GAME SELECT
    # =================================

    elif text in games:

        context.user_data["game"] = text

        keyboard = []

        for package in games[text]:
            keyboard.append([package])

        keyboard.append(["❌ Cancel"])

        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )

        await update.message.reply_text(
            f"💎 Choose Package For {text}",
            reply_markup=reply_markup
        )

        return

    # =================================
    # PACKAGE SELECT
    # =================================

    game = context.user_data.get("game")

    if game and text in games[game]:

        context.user_data["package"] = text

        price = games[game][text]

        context.user_data["price"] = price

        await update.message.reply_text(
            f"""
✅ Order Summary

🎮 Game: {game}

💎 Package: {text}

💰 Price: {price}

🆔 Send Your Game ID:
"""
        )

        context.user_data["waiting_game_id"] = True

        return

    # =================================
    # GAME ID
    # =================================

    if context.user_data.get("waiting_game_id"):

        context.user_data["game_id"] = text

        context.user_data["waiting_game_id"] = False

        await update.message.reply_text(
            """
💳 PAYMENT INFO

WavePay - 09xxxxxxxxx

📸 Send Payment Screenshot After Payment
"""
        )

        context.user_data["waiting_payment"] = True

        return

    # =================================
    # WAIT PAYMENT
    # =================================

    if context.user_data.get("waiting_payment"):

        await update.message.reply_text(
            "❌ Please send payment screenshot."
        )

        return


# =====================================
# PHOTO HANDLER
# =====================================

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.user_data.get("waiting_payment"):
        return

    user = update.effective_user

    photo = update.message.photo[-1].file_id

    game = context.user_data.get("game")
    package = context.user_data.get("package")
    price = context.user_data.get("price")
    game_id = context.user_data.get("game_id")

    username = user.username

    if username:
        username_text = f"@{username}"
    else:
        username_text = "No Username"

    caption = f"""
🛒 NEW ORDER

👤 Username: {username_text}

🆔 Telegram ID: {user.id}

🎮 Game: {game}

💎 Package: {package}

💰 Price: {price}

🎯 Game ID: {game_id}
"""

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✅ Confirm Order",
                callback_data=f"confirm_{user.id}"
            )
        ]
    ])

    # send to admin

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo,
        caption=caption,
        reply_markup=keyboard
    )

    await update.message.reply_text(
        """
✅ Payment Screenshot Sent

⏳ Waiting For Admin Confirm...
"""
    )

    context.user_data["waiting_payment"] = False


# =====================================
# BUTTON HANDLER
# =====================================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    data = query.data

    # =================================
    # CONFIRM ORDER
    # =================================

    if data.startswith("confirm_"):

        user_id = int(data.split("_")[1])

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "📦 Delivered",
                    callback_data=f"delivered_{user_id}"
                )
            ]
        ])

        # send to customer

        await context.bot.send_message(
            chat_id=user_id,
            text="""
✅ PAYMENT CONFIRMED

⏳ Your order is now processing.
"""
        )

        # edit admin message

        await query.edit_message_caption(
            caption=query.message.caption + "\n\n✅ PAYMENT CONFIRMED",
            reply_markup=keyboard
        )

    # =================================
    # DELIVERED
    # =================================

    elif data.startswith("delivered_"):

        user_id = int(data.split("_")[1])

        # send to customer

        await context.bot.send_message(
            chat_id=user_id,
            text="""
🎉 ORDER COMPLETED

✅ Your order has been delivered successfully.

❤️ Thank you for buying.
"""
        )

        # edit admin message

        await query.edit_message_caption(
            caption=query.message.caption + "\n\n📦 ORDER DELIVERED"
        )


# =====================================
# MAIN
# =====================================

def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            photo_handler
        )
    )

    app.add_handler(
        CallbackQueryHandler(button_handler)
    )

    print("✅ BOT RUNNING...")

    app.run_polling()


if __name__ == "__main__":
    main()
