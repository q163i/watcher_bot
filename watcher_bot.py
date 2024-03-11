import os
import telebot
import time
import argparse
import sys

TOKEN = os.getenv("TOKEN")
ALLOWED_USERS = [int(user_id) for user_id in os.getenv("ALLOWED_USERS", "").split(",") if user_id]

if not TOKEN or not ALLOWED_USERS:
    print("Error: TOKEN and ALLOWED_USERS cannot be empty.")
    sys.exit(1)

bot = telebot.TeleBot(TOKEN)

def send_message(chat_id, text):
    bot.send_message(chat_id, text)

def send_file(chat_id, file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            bot.send_document(chat_id, file)
    else:
        send_message(chat_id, "[System] File not found (404 error)")

def is_allowed_user(user_id):
    return user_id in ALLOWED_USERS

def handle_command_line_args():
    parser = argparse.ArgumentParser(description='Telegram bot with command line arguments.')
    parser.add_argument('command', nargs='?', default='run', help='Command to execute (default: run)')
    parser.add_argument('--data', help='Path to file')

    return parser.parse_args()

def run_bot():
    try:
        for user_id in ALLOWED_USERS:
            send_message(user_id, "[System] Bot started!")

        while True:
            try:
                bot.polling(none_stop=True)
            except Exception as e:
                print(f"ERROR: {e}")
                time.sleep(10)
    except Exception as e:
        print(f"ERROR: {e}")
        time.sleep(10)

if __name__ == '__main__':
    args = handle_command_line_args()

    if args.command == 'getData' and args.data:
        for user_id in ALLOWED_USERS:
            send_message(user_id, "[System] python3 watcher_bot.py getData --data * complete! ")
            send_file(user_id, args.data)
    elif args.command == 'run':
        run_bot()
    else:
        print("Invalid command. Usage: python3 watcher_bot.py [getData --data /path/file.env | run]")
