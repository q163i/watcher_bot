import os

# Telegram settings
TOKEN = os.getenv("TOKEN")  # Telegram bot token
ALLOWED_USERS = []
for user_id in os.getenv("ALLOWED_USERS", "").split(","):
    if user_id:
        try:
            ALLOWED_USERS.append(int(user_id))
        except ValueError:
            raise ValueError(f"Invalid user ID: {user_id}")

# Kubernetes settings
DEFAULT_KUBERNETES_API_URL = 'localhost'  # Default Kubernetes API URL
DEFAULT_KUBERNETES_API_TOKEN = 'blabla123'  # Default Kubernetes API token
KUBERNETES_API_URL = os.getenv("KUBERNETES_API_URL", DEFAULT_KUBERNETES_API_URL)  # Kubernetes API URL
KUBERNETES_API_TOKEN = os.getenv("KUBERNETES_API_TOKEN", DEFAULT_KUBERNETES_API_TOKEN)  # Kubernetes API token

# Database
DEFAULT_DB_USER = 'admin'  # Default database username
DEFAULT_DB_PASSWORD = 'admin'  # Default database password
DEFAULT_DB_HOST = 'localhost'  # Default database host
DEFAULT_DB_NAME = 'bot/db/mydatabase.db'  # Default database name for local noSQL database

DB_USER = os.getenv("DB_USER", DEFAULT_DB_USER)  # Database username
DB_PASSWORD = os.getenv("DB_PASSWORD", DEFAULT_DB_PASSWORD)  # Database password
DB_HOST = os.getenv("DB_HOST", DEFAULT_DB_HOST)  # Database host
DB_NAME = os.getenv("DB_NAME", DEFAULT_DB_NAME)  # Database name

# Logging
DEFAULT_LOG_LEVEL = "INFO"  # Default log level
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"  # Log format
LOG_LEVEL = os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL)  # Log level, can be set via environment variable