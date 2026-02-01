import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# FAKE TOKEN ONLY (replace with real token if you have)
TOKEN = "8551480846:AAFMWCSfF5xx1psTK1a5OVyfzIWjkSjNOH8"

users = {}          # user_id -> phone & balance
players = {}        # user_id -> cartela
called_numbers = []
game_running = False

MENU_OPTIONS = [
    ["Play", "Check Balance", "Contact Support"],
    ["Transfer", "Register", "Deposit"],
    ["Instruction", "Withdraw", "Invite"]
]

def make_bingo_number(n):
    if 1 <= n <= 15:
        return f"B-{n}"
    elif 16 <= n <= 30:
        return f"I-{n}"
    elif 31 <= n <= 45:
        return f"N-{n}"
    elif 46 <= n <= 60:
        return f"G-{n}"
    elif 61 <= n <= 75:
        return f"O-{n}"

# --- Start menu ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(opt, callback_data=opt) for opt in row] for row in MENU_OPTIONS]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Welcome to Ethiopian Bingo!\nChoose an option below:", reply_markup=reply_markup)

# --- Menu button handler ---
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    selection = query.data
    user_id = query.from_user.id

    if selection == "Register":
        keyboard = [[KeyboardButton("Share Phone Number", request_contact=True)]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        await query.message.reply_text("📝 Please share your phone number:", reply_markup=reply_markup)

    elif selection == "Play":
        keyboard = [[InlineKeyboardButton("Pick Cartela Number", url="https://docs.google.com/forms/d/e/YOUR_FORM_ID/viewform")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("🎲 Click the button below to choose your cartela number:", reply_markup=reply_markup)

    elif selection == "Check Balance":
        balance = users.get(user_id, {}).get("balance", 0)
        await query.message.reply_text(f"💰 Your balance: {balance} ETB")

    else:
        await query.message.reply_text(f"You selected: {selection}")

# --- Handle contact share ---
async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    user_id = update.message.from_user.id
    if contact:
        users[user_id] = users.get(user_id, {})
        users[user_id]["phone"] = contact.phone_number
        users[user_id]["balance"] = 0
        await update.message.reply_text(f"✅ Registration complete!\nPhone: {contact.phone_number}")

# --- Handle text messages (deposit example) ---
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

# --- Main function ---
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(menu_handler))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Ethiopian Bingo bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
