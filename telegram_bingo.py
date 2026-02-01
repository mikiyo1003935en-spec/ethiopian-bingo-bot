import random
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

players = {}
cards = {}
called = []
game_running = False


def generate_card():
    nums = random.sample(range(1, 76), 25)
    card = []
    for i in range(0, 25, 5):
        card.append(nums[i:i + 5])
    return card


def check_bingo(card, called):
    for row in card:
        if all(n in called for n in row):
            return True
    return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Ethiopian Bingo\n"
        "Join using:\n"
        "/join <cartela_number>\n"
        "Example: /join 105"
    )


async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global players, cards, game_running

    if game_running:
        await update.message.reply_text("Game already started.")
        return

    if len(players) >= 400:
        await update.message.reply_text("Game is full (400 players).")
        return

    if not context.args:
        await update.message.reply_text("Use: /join 105")
        return

    cartela = context.args[0]

    if cartela in players:
        await update.message.reply_text("This cartela is already taken.")
        return

    players[cartela] = update.effective_user.id
    cards[cartela] = generate_card()

    await update.message.reply_text(f"You joined with cartela {cartela}")


async def startgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game_running, called, players, cards

    if game_running:
        return

    if not players:
        await update.message.reply_text("No players yet.")
        return

    game_running = True
    called = []

    numbers = list(range(1, 76))
    random.shuffle(numbers)

    await update.message.reply_text("Bingo started!")

    for n in numbers:
        called.append(n)

        await update.message.reply_text(f"Number: {n}")

        for cartela, card in cards.items():
            if check_bingo(card, called):
                await update.message.reply_text(
                    f"BINGO !!!\nWinner cartela: {cartela}"
                )

                game_running = False
                players.clear()
                cards.clear()
                return

        await asyncio.sleep(4)


def main():
    app = Application.builder().token("8551480846:AAFMWCSfF5xx1psTK1a5OVyfzIWjkSjNOH8").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("join", join))
    app.add_handler(CommandHandler("startgame", startgame))

    app.run_polling()


if __name__ == "__main__":
    main()
