import os

# Telegram settings
TOKEN = os.getenv("TOKEN")  # Telegram bot token
ALLOWED_USERS = []
for user_id in os.getenv("ALLOWED_USERS", "").split(","):
    if user_id:
        ALLOWED_USERS.append(int(user_id))

## Kubernetes settings
# Create user and secret for Kubernetes:
# kubectl create serviceaccount my-service-account -n default
# kubectl create role my-role --verb="*" --resource="*" -n default
# kubectl create rolebinding my-rolebinding --role=my-role --serviceaccount=default:my-service-account -n default
# openssl genrsa -out my-service-account.key 2048
# openssl req -new -key my-service-account.key -out my-service-account.csr -subj "/CN=my-service-account/O=group1"
# openssl x509 -req -in my-service-account.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out my-service-account.crt -days 365
# kubectl create secret generic my-service-account-secret --from-literal=token=sadlkfjejp2oj34023 -n default
# kubectl patch serviceaccount my-service-account -p '{"imagePullSecrets": [{"name": "my-service-account-secret"}]}' -n default
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