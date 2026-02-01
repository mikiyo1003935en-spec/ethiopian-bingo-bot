from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import asyncio, random

# Fake token for example
TOKEN = "8551480846:AAFMWCSfF5xx1psTK1a5OVyfzIWjkSjNOH8"

# Track users and their info
users = {}  # user_id -> {"phone": ..., "balance": ..., "cartela": ...}

# Menu options
MENU_OPTIONS = [
    ["Play", "Check Balance", "Contact Support"],
    ["Transfer", "Register", "Deposit"],
    ["Instruction", "Withdraw", "Invite"]
]

# Track called numbers for live bingo
called_numbers = []
game_running = False

# Start command and menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(opt, callback_data=opt) for opt in row] for row in MENU_OPTIONS]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Welcome to Ethiopian Bingo!\nChoose an option below:", reply_markup=reply_markup)

# Menu button handler
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    selection = query.data
    user_id = query.from_user.id

    # Register
    if selection == "Register":
        keyboard = [[KeyboardButton("Share Phone Number", request_contact=True)]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await query.edit_message_text("📝 Please share your phone number:", reply_markup=reply_markup)

    # Check balance
    elif selection == "Check Balance":
        balance = users.get(user_id, {}).get("balance", 0)
        await query.edit_message_text(f"💰 Your balance: {balance} ETB")

    # Deposit
    elif selection == "Deposit":
        await query.edit_message_text("➕ Enter deposit amount (just type a number):")

    # Withdraw
    elif selection == "Withdraw":
        await query.edit_message_text("➖ Enter withdraw amount (just type a number):")

    # Invite
    elif selection == "Invite":
        await query.edit_message_text("📨 Share this bot link: t.me/YourBotUsername")

    # Play
    elif selection == "Play":
        keyboard = [[InlineKeyboardButton(
            "Pick Cartela Number",
            url="https://docs.google.com/forms/d/e/1FAIpQLSfFBWY4mU8wq-XF2XvoX2jbLnS5fUHS-Lr7HELjAIBtmY754g/viewform?usp=publish-editor"
        )]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🎲 Click below to choose your cartela number:",
            reply_markup=reply_markup
        )

    else:
        await query.edit_message_text(f"You selected: {selection}")

# Handle phone contact
async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    user_id = update.message.from_user.id
    if contact:
        users[user_id] = users.get(user_id, {})
        users[user_id]["phone"] = contact.phone_number
        users[user_id]["balance"] = 0
        await update.message.reply_text(f"✅ Registration complete!\nPhone: {contact.phone_number}")

# Handle text messages for deposit/withdraw
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id
    if text.isdigit():
        amount = int(text)
        users[user_id] = users.get(user_id, {})
        users[user_id]["balance"] = users[user_id].get("balance", 0) + amount
        await update.message.reply_text(f"✅ Deposit successful! New balance: {users[user_id]['balance']} ETB")
    else:
        await update.message.reply_text("❌ Please enter a valid number.")

# Run bot
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(menu_handler))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
