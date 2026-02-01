import random
import time

players = {}

def generate_card():
    numbers = random.sample(range(1, 76), 25)
    card = []
    for i in range(0, 25, 5):
        card.append(numbers[i:i+5])
    return card

def print_card(card):
    for row in card:
        print(" ".join(f"{n:2}" for n in row))

def create_player():
    name = input("Enter player name: ")
    card = generate_card()
    players[name] = card
    print("\nCartela for", name)
    print_card(card)
    print()

def check_bingo(card, called):
    for row in card:
        if all(n in called for n in row):
            return True
    return False

def start_bingo():
    called = []
    numbers = list(range(1, 76))
    random.shuffle(numbers)

    print("\nBingo started...")

    for n in numbers:
        called.append(n)
        print("Number:", n)

        for name, card in players.items():
            if check_bingo(card, called):
                print("\n*************")
                print("BINGO !!!")
                print("Winner:", name)
                print("*************")
                return

        time.sleep(3)

def main():
    while True:
        print("\n--- Ethiopian Bingo System ---")
        print("1. Add player")
        print("2. Start bingo")
        print("3. Exit")

        choice = input("Select: ")

        if choice == "1":
            create_player()
        elif choice == "2":
            if not players:
                print("No players yet.")
            else:
                start_bingo()
        elif choice == "3":
            break

main()
