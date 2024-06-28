import os, telebot, sys, logging, argparse

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import configs
TOKEN = os.getenv('TOKEN')
ALLOWED_USERS = os.getenv('ALLOWED_USERS')

if not TOKEN or not ALLOWED_USERS:
    logger.error("Error: ENV: TOKEN and ENV: ALLOWED_USERS cannot be empty")
    sys.exit(1)

bot = telebot.TeleBot(TOKEN)

# Create a parser for command line arguments
parser = argparse.ArgumentParser(description='This script allows you to send deployment status messages to a Telegram chat.')
parser.add_argument('command', help='The command to execute. Available commands are: infoDeploySuccess, infoDeployFail')
parser.add_argument('--text', help='The text to send. If not provided, a default message will be sent.')
parser.add_argument('--path', help='The path to the file to send.')
parser.add_argument('--adminChat', help='The chat ID to send the file or message to. If not provided, ALLOWED_USERS will be used.')

args = parser.parse_args()

def replace_env_variables(text):
    for key, value in os.environ.items():
        text = text.replace(f"${key}", value)
    return text

def infoDeploySuccess():
    try:
        admin_chat = ALLOWED_USERS
        text = args.text if args.text else f"```🟢CI/CD\nProject: $GITHUB_REPOSITORY\nVersion: $GITHUB_REF\nCommit: $GITHUB_COMMIT_MESSAGE\nAuthor: $GITHUB_ACTOR\nSTATUS: $GITHUB_BUILD_STATUS\n```"
        text = replace_env_variables(text)
        bot.send_message(admin_chat, text, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error: {e}")
        logger.error("Usage: python3 ./bot/SimpleMessage.py infoDeploySuccess --text \"<text>\"")

def infoDeployFail():
    try:
        admin_chat = ALLOWED_USERS
        text = args.text if args.text else f"```🔴CI/CD\nProject: $GITHUB_REPOSITORY\nVersion: $GITHUB_REF\nCommit: $GITHUB_COMMIT_MESSAGE\nAuthor: $GITHUB_ACTOR\nSTATUS: $GITHUB_BUILD_STATUS\n```"
        link = f"Details: https://github.com/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID"
        text = replace_env_variables(text)
        link = replace_env_variables(link)
        bot.send_message(admin_chat, text, parse_mode='Markdown')
        bot.send_message(admin_chat, link)
    except Exception as e:
        logger.error(f"Error: {e}")
        logger.error("Usage: python3 ./bot/SimpleMessage.py infoDeployFail --text \"<text>\"")

# Update your sendFile function to use the path argument
def sendFile():
    try:
        file_path = args.path
        admin_chat = args.adminChat if args.adminChat else ALLOWED_USERS
        with open(file_path, 'rb') as file:
            bot.send_document(admin_chat, file)
        logger.info(f"File {file_path} sent to chat {admin_chat}")
    except Exception as e:
        logger.error(f"Error: {e}")
        logger.error("Usage: python3 ./bot/SimpleMessage.py sendFile --path <path> [--adminChat <adminChat>]")

# Update your main function to call sendFile when the command is 'sendFileToUser'
if __name__ == '__main__':
    if args.command == 'infoDeploySuccess':
        infoDeploySuccess()
    elif args.command == 'infoDeployFail':
        infoDeployFail()
    elif args.command == 'sendFileToUser':
        sendFile()