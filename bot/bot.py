# Import Logging
from LoggerConfig import custom_logger
logger = custom_logger()

# Import AdminCommands
from AdminCommands import *

# Import configs
from config import TOKEN, ALLOWED_USERS

import telebot, sys, time

bot = telebot.TeleBot(TOKEN)

if not TOKEN or not ALLOWED_USERS:
    logger.error("Error: ENV: TOKEN and ENV: ALLOWED_USERS cannot be empty")
    sys.exit(1)

def telegram_bot():
    try:
        logger.info("[System] Join Telegram bot (backend) thread")
        while True:
            try:
                bot.polling(none_stop=True)
            except Exception as e:
                logger.info(f"[System] Bot encountered an error: {e}")
                time.sleep(5)
    except Exception as e:
        logger.info(f"[System] Error: {e}")
        time.sleep(5)

# Added the following lines
AdminCommands = AdminCommands(bot)

# AdminCommands
AdminCommands.help()
AdminCommands.get_id()
AdminCommands.admin_list()
AdminCommands.admin_complete()
AdminCommands.admin_add()
AdminCommands.admin_remove()
AdminCommands.blocked_users_list()

# InfraCommands
AdminCommands.info()
AdminCommands.get_ip()
AdminCommands.check_port()
AdminCommands.check_certificate()
AdminCommands.check_disk_space()
AdminCommands.check_cpu_usage()
AdminCommands.check_memory_usage()
AdminCommands.check_environment()
# k8s commands
AdminCommands.get_pods()
AdminCommands.get_k8s_settings()
AdminCommands.delete_project()


if __name__ == '__main__':
    telegram_bot()