# Import Logging
from LoggerConfig import custom_logger
logger = custom_logger()

# Import the Telegram bot from the bot file
from bot import telegram_bot

# Import the create_database function from the db file
from db import database

import threading, time

# If this file is the entry point to the application
if __name__ == "__main__":
    logger.info("********************************")
    logger.info("***  Welcome to Watcher Bot! ***")
    logger.info("********************************")
    # Create the database
    database()
    # Wait for the Telegram bot thread to finish

    # Create a thread for the Telegram bot
    bot_thread = threading.Thread(target=telegram_bot)
    # flask_thread = threading.Thread(target=app.run)

    # BACKEND
    # Start the Telegram bot thread
    bot_thread.start()
    # Wait for the Telegram bot thread to finish
    while not bot_thread.is_alive():
        time.sleep(1)

    # FRONTEND
    # Start the Flask application thread
    # logger.info("[System] Join Flask app (frontend) thread")
    # flask_thread.start()

    # Wait for the Flask application thread to finish
    bot_thread.join()
    # flask_thread.join()
