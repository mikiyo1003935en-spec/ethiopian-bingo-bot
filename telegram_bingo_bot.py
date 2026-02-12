import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# ENTER YOUR BOT TOKEN HERE
import os
TOKEN = os.environ.get("8551480846:AAFMWCSfF5xx1psTK1a5OVyfzIWjkSjNOH8")

users = {}
players = {}
called_numbers = []
game_running = False

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Ethiopian Bingo bot 🎯\n\nUse /startgame to start a demo game."
    )

async def startgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game_running, called_numbers
    game_running = True
    called_numbers = []
    await update.message.reply_text("Bingo game started ✅")

async def call(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global called_numbers, game_running
    if not game_running:
        await update.message.reply_text("Game is not running.")
        return
    remaining = list(set(range(1, 76)) - set(called_numbers))
    if not remaining:
        await update.message.reply_text("All numbers are called.")
        return
    num = random.choice(remaining)
    called_numbers.append(num)
    await update.message.reply_text(f"Next number: {make_bingo_number(num)}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("startgame", startgame))
    app.add_handler(CommandHandler("call", call))
    print("Bingo bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
