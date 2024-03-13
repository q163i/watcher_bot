import os
import telebot
import argparse
import sys
import subprocess
from threading import Timer
from datetime import datetime
import ssl
from urllib.parse import urlparse
import socket
import logging
import requests

restart_notification = os.getenv("RESTART_NOTIFICATION", "false")

if restart_notification.lower() == "true":
    for user_id in ALLOWED_USERS:
        logging.info("[System] Bot restarted after update!")
        send_message(user_id, "[System] Bot restarted after update!")

DEFAULT_LOG_LEVEL = "INFO"
LOG_LEVEL = os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL)

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

LOG_FILE = os.getenv("LOG_FILE")  # Get log file path from environment variable

# Configure logging to write to both stdout and a file
handlers = [logging.StreamHandler()]  # Always write logs to stdout
if LOG_FILE:
    handlers.append(logging.FileHandler(LOG_FILE))  # Add file handler if LOG_FILE is provided
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, handlers=handlers)

TOKEN = os.getenv("TOKEN")
ALLOWED_USERS = [int(user_id) for user_id in os.getenv("ALLOWED_USERS", "").split(",") if user_id]

if not TOKEN or not ALLOWED_USERS:
    logging.error("Error: TOKEN and ALLOWED_USERS cannot be empty.")
    sys.exit(1)

bot = telebot.TeleBot(TOKEN)

# Определение функции send_file
def send_file(chat_id, file_path):
    logging.info(f"Sending file {file_path} to {chat_id}")
    with open(file_path, 'rb') as file:
        bot.send_document(chat_id, file)

def send_message(chat_id, text):
    logging.info(f"Sending message to {chat_id}: {text}")
    bot.send_message(chat_id, text)

@bot.message_handler(func=lambda message: not is_allowed_user(message.chat.id))
def handle_unauthorized_message(message):
    error_message = "[System] 403 - Forbidden. You are not in the list of ALLOWED_USERS."
    logging.error(error_message)
    send_message(message.chat.id, error_message)
    forward_spam_message(message)

def forward_spam_message(message):
    for user_id in ALLOWED_USERS:
        if user_id != message.chat.id:
            logging.info(f"[System] Forwarding spam message to ALLOWED_USERS: {ALLOWED_USERS}")
            send_message(user_id, f"[Spam] Message from unauthorized user (ID: {message.chat.id}): {message.text}")

def is_allowed_user(user_id):
    return user_id in ALLOWED_USERS

def handle_command_line_args():
    parser = argparse.ArgumentParser(description='Telegram bot with command line arguments.')
    parser.add_argument('command', nargs='?', default='run', help='Command to execute (default: run)')
    parser.add_argument('--data', help='Path to file')

    return parser.parse_args()

def get_external_ip():
    try:
        # Сервис, предоставляющий информацию о внешнем IP-адресе
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text  # Получаем внешний IP-адрес из ответа
        else:
            logging.error(f"Failed to retrieve external IP address: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Error retrieving external IP address: {e}")
        return None

def run_bot():
    try:
        logging.info("[System] Bot started!")

        # Получаем внешний IP-адрес при запуске бота
        external_ip = get_external_ip()
        if external_ip:
            for user_id in ALLOWED_USERS:
                send_message(user_id, f"[System] Bot started! External IP: {external_ip}")

        while True:
            try:
                bot.polling(none_stop=True)
            except Exception as e:
                logging.error(f"Bot encountered an error: {e}")
                time.sleep(10)
    except Exception as e:
        logging.error(f"Error: {e}")
        time.sleep(10)

def send_help_message(chat_id):
    help_text = "/help - Show available commands\n"
    help_text += "/checkNetwork <server> <port> - Check network availability to the specified server and port (e.g., /checkNetwork 8.8.8.8 443)\n"
    help_text += "/checkCertificate <domain_name> - Check SSL certificate expiration date for the specified domain (e.g., /checkCertificate https://google.com)\n"
    help_text += "\n"
    help_text += "Command executed from the server: python3 watcher_bot.py getData --data /path/to/file.exe - send a file from the server to Telegram\n"
    send_message(chat_id, help_text)

@bot.message_handler(commands=['help'])
def handle_help(message):
    if is_allowed_user(message.chat.id):
        send_help_message(message.chat.id)

@bot.message_handler(commands=['checkNetwork'])
def handle_check_network(message):
    if is_allowed_user(message.chat.id):
        try:
            _, server, port = message.text.split()

            # Run the network check command with a timeout of 3 seconds
            process = subprocess.Popen(['nc', '-vnz', '-w', '3', server, port], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            timer = Timer(3, process.kill)

            try:
                timer.start()
                stdout, stderr = process.communicate()
            finally:
                timer.cancel()

            if process.returncode == 0:
                send_message(message.chat.id, f"[System] Network check result: Port {port} is available on {server}")
            else:
                send_message(message.chat.id, f"[System] Network check result: Port {port} is not available on {server}")
        except ValueError:
            send_message(message.chat.id, "[System] Incorrect command format. Use /checkNetwork <server> <port>")
    else:
        forward_spam_message(message)

@bot.message_handler(commands=['checkCertificate'])
def handle_check_certificate(message):
    if is_allowed_user(message.chat.id):
        try:
            _, domain = message.text.split()
            expiration_days = get_certificate_expiration_days(domain)
            if expiration_days is not None:
                send_message(message.chat.id, f"[System] SSL certificate for {domain} expires in {expiration_days} days.")
            else:
                send_message(message.chat.id, f"[System] Unable to retrieve SSL certificate information for {domain}.")
        except ValueError:
            send_message(message.chat.id, "[System] Incorrect command format. Use /checkCertificate <domain_name>")
    else:
        forward_spam_message(message)

@bot.message_handler(commands=['start'])
def handle_start(message):
    if is_allowed_user(message.chat.id):
        handle_help(message)

def get_certificate_expiration_days(domain):
    try:
        url = urlparse(domain)
        hostname = url.netloc

        context = ssl.create_default_context()
        with context.wrap_socket(socket.create_connection((hostname, 443)), server_hostname=hostname) as sock:
            cert = sock.getpeercert()

        expiration_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
        days_until_expiration = (expiration_date - datetime.utcnow()).days
        return days_until_expiration
    except Exception as e:
        logging.error(f"Error retrieving SSL certificate information: {e}")
        return None

if __name__ == '__main__':
    args = handle_command_line_args()

    if args.command == 'getData' and args.data:
        for user_id in ALLOWED_USERS:
            send_message(user_id, "[System] python3 watcher_bot.py getData --data * completed! ")
            send_file(user_id, args.data)
    elif args.command == 'run':
        run_bot()
    else:
        logging.error("Invalid command. Usage: python3 watcher_bot.py [getData --data /pathto/file.env | run]")
