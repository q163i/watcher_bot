# Watcher_bot

This repository contains a simple Telegram bot written in Python using the `pyTelegramBotAPI` library. 
The bot is designed to perform specific actions based on command line arguments and interact with authorized users.

### Build on M1
   ```bash
docker build --platform linux/amd64 -t q163i/watcher_bot:1 .
   ```

## Bot Logic

### Dependencies
- pyTelegramBotAPI==3.7.7

### How It Works

1. **Environment Variables:**
   - The bot relies on the following environment variables:
      - `TOKEN`: Telegram bot token.
      - `ALLOWED_USERS`: Comma-separated list of user IDs allowed to interact with the bot.

2. **Bot Initialization:**
   - The bot is initialized using the provided token.

3. **Command Line Arguments:**
   - The bot supports the following command line arguments:
      - `run`: Start the bot and listen for incoming messages.
      - `getData --data /path/file.env`: Execute a command to send a message and a file to authorized users.

4. **Bot Commands:**
   - The bot responds to the `/getData` command by sending a message to authorized users and attaching a file specified by the `--data` argument.

5. **Error Handling:**
   - The bot includes error handling to catch exceptions during the execution and prints error messages.

### Docker Setup (Unix)

1. **Build Docker Image:**
   - Use the provided Dockerfile to build the image. Make sure to have the required dependencies installed.

   ```bash
   docker build -t watcherbot:1 .

# Todo
1. Add normal README.md
2. Add /help
3. Add other command with run -d 