import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Bot token directly
TOKEN = "8551480846:AAFMWCSfF5xx1psTK1a5OVyfzIWjkSjNOH8"

# Game data
users = {}
players = {}
called_numbers = []
game_running = False

# Function to generate bingo number
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
    else:
        return None

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to Ethiopian Bingo Bot! Type /join to play.")

# /join command
async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in players:
        await update.message.reply_text("You have already joined the game!")
    else:
        players[user_id] = {"name": update.message.from_user.first_name}
        await update.message.reply_text(f"{update.message.from_user.first_name} joined the game!")

# Main function
def main():
    app = Application.builder().token(TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("join", join))

    print("Bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
