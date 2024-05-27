# Import Logging
from LoggerConfig import custom_logger
# Create a logger instance
logger = custom_logger()

# Import the necessary modules for database operations
from GetEngine import Database
from AdminImport import Admins
from DefineTables import BlockedUsers

# for k8s
from kubernetes import client, config
from tabulate import tabulate

# Infra
import socket, subprocess, ssl, os
from datetime import datetime
from urllib.parse import urlparse

# Create a database instance
db = Database()
# Create a session for database operations
Session = db.Session

# Define a class for handling bot admin commands
class AdminCommands:
    # Initialize the class with a bot instance
    def __init__(self, bot):
        self.bot = bot
        self.namespaces = {}  # Add this line
        self.info()

    def info(self):
        @self.bot.message_handler(commands=['info'])
        def _info(message):
            # Check if the user is an admin
            if not self.is_admin(message.from_user.id):
                return
            # Define the project information
            project_info = """
            Project: watcher-bot
            Author: Roman Litvinov
            GitHub Repository: https://github.com/q163i/watcher_bot
            Suggestions: Feel free to contribute to the project by opening issues or submitting pull requests.
            """
            # Send the project information to the user
            self.bot.reply_to(message, project_info)
            # Log the execution of the info command
            logger.info(f"{message.from_user.id}: /info command executed")

    # Method to check if a user is an admin
    def is_admin(self, user_id):
        # Open a database session
        session = Session()
        # Query the database for the user
        admin = session.query(Admins).filter(Admins.telegram_id == user_id).first()
        # Close the database session
        session.close()
        # Return True if the user is an admin, False otherwise
        if admin:
            return True
        else:
            return False

    def check_environment(self):
        @self.bot.message_handler(commands=['checkEnvironment'])
        def _check_environment(message):
            # Check if the user is an admin
            if not self.is_admin(message.from_user.id):
                return
            # Check if running in Docker
            if os.path.exists('/proc/1/cgroup'):
                with open('/proc/1/cgroup', 'rt') as ifh:
                    if 'docker' in ifh.read():
                        self.bot.reply_to(message, "[System] The bot is running in a Docker container.")
                        return
            # Check if running in Kubernetes
            if os.getenv('KUBERNETES_SERVICE_HOST'):
                self.bot.reply_to(message, "[System] The bot is running in Kubernetes.")
                return
            # If not running in Docker or Kubernetes
            self.bot.reply_to(message, "[System] The bot is not running in Docker or Kubernetes.")
            logger.info(f"{message.from_user.id}: /checkEnvironment command executed")

    def help(self):
        @self.bot.message_handler(commands=['help', 'start'])
        def _help(message):
            user_id = message.from_user.id
            help_text = """
            Here are the commands you can use:
            /getID - Get your ID and chat ID (work for private chat only) - for all
            /adminList - Get a list of all admins
            /adminComplete - Update usernames
            /adminAdd - Add a new admin. Usage: /adminAdd <telegram_id>
            /adminRemove - Remove an admin. Usage: /adminRemove <telegram_id>
            /blockedUsersList - Get a list of the last 5 blocked users
            /getIP - Get the server IP address
            /checkPort - Check if a port is open on a server. Usage: /checkPort <server_ip> <port>
            /checkCertificate - Check the SSL certificate of a website. Usage: /checkCertificate <url>
            /checkDiskSpace - Check the disk space usage on the server
            /checkCPUUsage - Check the CPU usage on the server
            /checkMemoryUsage - Check the memory usage on the server
            /checkEnvironment - Check if the bot is running in Docker or Kubernetes
            /getK8sSettings - Set the Kubernetes namespace for future commands
            /getPods - Get a list of pods in the set namespace
            /deleteProject - Delete a project and all related resources in the set namespace. Usage: /deleteProject <project_name>
            """
            self.bot.reply_to(message, help_text)
            logger.info(f"{user_id}: /help command executed")

    # Define the get_id command
    def get_id(self):
        @self.bot.message_handler(commands=['getID'])
        def _get_id(message):
            # Get the user's ID and chat ID
            user_id = message.from_user.id
            chat_id = message.chat.id
            # Send the IDs to the user
            self.bot.reply_to(message, f"[System] Your ID is {user_id}, your chat ID is {chat_id}")
            # Log the execution of the get_id command
            logger.info(f"{user_id}: /getID command executed")

    # Define the admin_list command
    def admin_list(self):
        @self.bot.message_handler(commands=['adminList'])
        def _admin_list(message):
            # Check if the user is an admin
            if not self.handle_message(message):
                return
            # Get the user's ID
            user_id = message.from_user.id
            # Open a database session
            session = Session()
            # Query the database for all admins
            admins = session.query(Admins).all()
            # Create a list of all admins
            admin_list = "\n".join(
                [f"{i + 1}. {admin.username} ({admin.telegram_id})" for i, admin in enumerate(admins)])
            # Send the list to the user
            self.bot.reply_to(message, admin_list)
            # Close the database session
            session.close()
            # Log the execution of the admin_list command
            logger.info(f"{user_id}: /adminList command executed")

    # Define the complete_usernames command
    def complete_usernames(self):
        # Open a database session
        session = Session()
        # Query the database for all admins
        admins = session.query(Admins).all()
        # Update the username of each admin
        for admin in admins:
            user_info = self.bot.get_chat(admin.telegram_id)
            admin.username = user_info.username
        # Commit the changes to the database
        session.commit()
        # Close the database session
        session.close()
        # Log the execution of the complete_usernames command
        logger.info("[System] Usernames updated")

    # Define the admin_complete command
    def admin_complete(self):
        @self.bot.message_handler(commands=['adminComplete'])
        def _admin_complete(message):
            # Check if the user is an admin
            if not self.handle_message(message):
                return
            # Get the user's ID
            user_id = message.from_user.id
            # Update the usernames of all admins
            self.complete_usernames()
            # Notify the user that the usernames have been updated
            self.bot.reply_to(message, "[System] Usernames updated")
            # Log the execution of the admin_complete command
            logger.info(f"{user_id}: /adminComplete command executed")

    # Define the admin_add command
    def admin_add(self):
        @self.bot.message_handler(commands=['adminAdd'])
        def _admin_add(message):
            # Check if the user is an admin
            if not self.handle_message(message):
                return
            # Get the user's ID
            user_id = message.from_user.id
            # Split the message into parts
            split_message = message.text.split()
            # Check if the command format is correct
            if len(split_message) < 2:
                self.bot.reply_to(message, "[System] Invalid command format. Usage: /adminAdd <telegram_id>")
                return
            # Get the telegram_id from the message
            telegram_id = split_message[1]
            # Open a database session
            session = Session()
            # Create a new Admin object
            new_admin = Admins(telegram_id=telegram_id)
            # Add the new admin to the session
            session.add(new_admin)
            # Commit the changes to the database
            session.commit()
            # Notify the user that the new admin has been added
            self.bot.reply_to(message, f"[System] Added new admin with ID {telegram_id}")
            # Close the database session
            session.close()
            # Log the execution of the admin_add command
            logger.info(f"{user_id}: /adminAdd command executed with ID {telegram_id}")

    # Define the admin_remove command
    def admin_remove(self):
        @self.bot.message_handler(commands=['adminRemove'])
        def _admin_remove(message):
            # Check if the user is an admin
            if not self.handle_message(message):
                return
            # Get the user's ID
            user_id = message.from_user.id
            # Split the message into parts
            split_message = message.text.split()
            # Check if the command format is correct
            if len(split_message) < 2:
                self.bot.reply_to(message, "[System] Invalid command format. Usage: /adminRemove <telegram_id>")
                return
            # Get the telegram_id from the message
            telegram_id = split_message[1]
            # Open a database session
            session = Session()
            # Query the database for the admin
            admin = session.query(Admins).filter(Admins.telegram_id == telegram_id).first()
            # Check if the admin exists
            if admin:
                # Delete the admin from the session
                session.delete(admin)
                # Commit the changes to the database
                session.commit()
                # Notify the user that the admin has been removed
                self.bot.reply_to(message, f"[System] Removed admin with ID {telegram_id}")
            else:
                # Notify the user that the admin was not found
                self.bot.reply_to(message, f"[System] No admin found with ID {telegram_id}")
            # Close the database session
            session.close()
            # Log the execution of the admin_remove command
            logger.info(f"{user_id}: /adminRemove command executed with ID {telegram_id}")

    # Define the handle_message method
    def handle_message(self, message):
        # Get the user's ID and username
        user_id = message.from_user.id
        username = message.from_user.username
        # Check if the user is an admin
        if self.is_admin(user_id):
            return True
        else:
            # Block the user
            self.block_user(user_id, username, message.text)
            return False

    # Define the block_user method
    def block_user(self, user_id, username, message):
        # Open a database session
        session = Session()
        # Create a new BlockedUsers object
        blocked_user = BlockedUsers(telegram_id=user_id, username=username, message=message)
        # Add the blocked user to the session
        session.add(blocked_user)
        # Commit the changes to the database
        session.commit()
        # Close the database session
        session.close()
        # Log the execution of the block_user method
        logger.info(f"{user_id}: User blocked trying to execute command or send message: '{message}'")

    # Define the blocked_users_list command
    def blocked_users_list(self):
        @self.bot.message_handler(commands=['blockedUsersList'])
        def _blocked_users_list(message):
            # Check if the user is an admin
            if not self.handle_message(message):
                return
            # Get the user's ID
            user_id = message.from_user.id
            # Open a database session
            session = Session()
            # Query the database for the last 5 blocked users
            blocked_users = session.query(BlockedUsers).order_by(BlockedUsers.timestamp.desc()).limit(5).all()
            # Create a list of the blocked users
            blocked_users_list = "\n".join(
                [f"{i + 1}. {user.username} ({user.telegram_id}) - {user.message} - {user.timestamp}" for i, user in
                 enumerate(blocked_users)])
            # Send the list to the user
            self.bot.reply_to(message, blocked_users_list)
            # Close the database session
            session.close()
            # Log the execution of the blocked_users_list command
            logger.info(f"{user_id}: /blockedUsersList command executed")

    def get_ip(self):
        @self.bot.message_handler(commands=['getIP'])
        def _get_ip(message):
            # Check if the user is an admin
            if not self.is_admin(message.from_user.id):
                return
            # Get the host name of the machine where the Python interpreter is executed
            host_name = socket.gethostname()
            # Get the IP address corresponding to the host name
            ip_address = socket.gethostbyname(host_name)
            # Send the IP address to the user
            self.bot.reply_to(message, f"[System] Server IP address: {ip_address}")
            # Log the execution of the get_ip command
            logger.info(f"{message.from_user.id}: /getIP command executed")

    def check_port(self):
        @self.bot.message_handler(commands=['checkPort'])
        def _check_port(message):
            # Check if the user is an admin
            if not self.is_admin(message.from_user.id):
                return
            # Split the message into parts
            split_message = message.text.split()
            # Check if the command format is correct
            if len(split_message) < 3:
                self.bot.reply_to(message, "[System] Invalid command format. Usage: /checkPort <server_ip> <port>")
                return
            # Get the server_ip and port from the message
            server_ip, port = split_message[1], split_message[2]
            # Form the command
            command = ['nc', '-vnz', server_ip, port]
            try:
                # Execute the command and capture both stdout and stderr with a timeout of 5 seconds
                result = subprocess.run(command, capture_output=True, text=True, timeout=5)
                # Send the result to the user
                if result.stdout:
                    self.bot.reply_to(message, f"[System] Command result: {result.stdout}")
                if result.stderr:
                    self.bot.reply_to(message, f"[System] Command error: {result.stderr}")
            except subprocess.TimeoutExpired:
                self.bot.reply_to(message, f"[System] Command timed out after 5 seconds")
            # Log the execution of the check_port command
            logger.info(f"{message.from_user.id}: /checkPort {server_ip} {port}")

    def check_certificate(self):
        @self.bot.message_handler(commands=['checkCertificate'])
        def _check_certificate(message):
            # Check if the user is an admin
            if not self.is_admin(message.from_user.id):
                return
            # Split the message into parts
            split_message = message.text.split()
            # Check if the command format is correct
            if len(split_message) < 2:
                self.bot.reply_to(message, "[System] Invalid command format. Usage: /checkCertificate <url>")
                return
            # Get the url from the message
            url = split_message[1]
            # Parse the url to extract the hostname
            hostname = urlparse(url).hostname
            # Create a new SSL context with secure default settings
            context = ssl.create_default_context()
            try:
                # Create a new socket
                with socket.create_connection((hostname, 443)) as sock:
                    # Wrap the socket in an SSL context
                    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                        # Get the certificate
                        cert = ssock.getpeercert()
                # Check if the 'notAfter' field is in the certificate
                if 'notAfter' in cert:
                    # Get the notAfter field from the certificate
                    not_after = cert['notAfter']
                    # Parse the notAfter field to a datetime object
                    not_after = datetime.strptime(not_after, r'%b %d %H:%M:%S %Y %Z')
                    # Get the current date
                    now = datetime.now()
                    # Calculate the number of days until the certificate expires
                    days_until_expiration = (not_after - now).days
                    # Send the number of days until expiration to the user
                    self.bot.reply_to(message, f"[System] Certificate for {url} is valid for {days_until_expiration} more days.")
                else:
                    # Send a message to the user indicating that the certificate is not valid
                    self.bot.reply_to(message, f"[System] Certificate for {url} is not valid.")
            except socket.gaierror:
                self.bot.reply_to(message, f"[System] Could not resolve hostname: {url}")
            # Log the execution of the check_certificate command
            logger.info(f"{message.from_user.id}: /checkCertificate {url}")


    def check_disk_space(self):
        @self.bot.message_handler(commands=['checkDiskSpace'])
        def _check_disk_space(message):
            if not self.is_admin(message.from_user.id):
                return
            result = subprocess.run(['df', '-h'], capture_output=True, text=True)
            self.bot.reply_to(message, f"[System] Disk space usage:\n{result.stdout}")
            logger.info(f"{message.from_user.id}: /checkDiskSpace command executed")

    def check_cpu_usage(self):
        @self.bot.message_handler(commands=['checkCPUUsage'])
        def _check_cpu_usage(message):
            if not self.is_admin(message.from_user.id):
                return
            result = subprocess.run(['top', '-b', '-n1'], capture_output=True, text=True)
            self.bot.reply_to(message, f"[System] CPU usage:\n{result.stdout}")
            logger.info(f"{message.from_user.id}: /checkCPUUsage command executed")

    def check_memory_usage(self):
        @self.bot.message_handler(commands=['checkMemoryUsage'])
        def _check_memory_usage(message):
            if not self.is_admin(message.from_user.id):
                return
            result = subprocess.run(['free', '-h'], capture_output=True, text=True)
            self.bot.reply_to(message, f"[System] Memory usage:\n{result.stdout}")
            logger.info(f"{message.from_user.id}: /checkMemoryUsage command executed")

# K8S
    def get_k8s_settings(self):
        @self.bot.message_handler(commands=['getK8sSettings'])
        def _get_k8s_settings(message):
            if not self.is_admin(message.from_user.id):
                return
            config.load_kube_config()
            v1 = client.CoreV1Api()
            namespaces = v1.list_namespace()
            namespaces_list = [ns.metadata.name for ns in namespaces.items]
            namespaces_str = ', '.join(namespaces_list)
            msg = self.bot.reply_to(message,
                                    f"[System] Available namespaces: {namespaces_str}\nPlease enter the namespace for future actions:")
            self.bot.register_next_step_handler(msg, self.k8s_save_namespace)
            logger.info(
                f"{message.from_user.id}: /getK8sSettings command executed. Available namespaces: {namespaces_str}")

    def k8s_save_namespace(self, message):
        namespace = message.text
        config.load_kube_config()
        v1 = client.CoreV1Api()
        existing_namespaces = [ns.metadata.name for ns in v1.list_namespace().items]
        if namespace in existing_namespaces:
            self.namespaces[message.from_user.id] = namespace
            self.bot.reply_to(message, f"[System] Namespace '{namespace}' saved successfully.")
            logger.info(f"{message.from_user.id}: Namespace '{namespace}' saved successfully.")
        else:
            self.bot.reply_to(message,
                              f"[System] Namespace '{namespace}' does not exist. Context selected but namespace does not exist yet.")
            logger.info(f"{message.from_user.id}: Attempted to save non-existing namespace '{namespace}'.")

    def get_pods(self):
        @self.bot.message_handler(commands=['getPods'])
        def _get_pods(message):
            if not self.is_admin(message.from_user.id):
                return
            namespace = self.namespaces.get(message.from_user.id)
            if not namespace:
                self.bot.reply_to(message, "[System] Please set the namespace first using /getK8sSettings")
                return
            try:
                config.load_kube_config()
                v1 = client.CoreV1Api()
                pods = v1.list_namespaced_pod(namespace)
                pods_list = [[i.metadata.name, i.metadata.namespace] for i in pods.items]
                table = tabulate(pods_list, headers=['Name', 'Namespace'], tablefmt='pretty')
                self.bot.reply_to(message, f"Namespace: {namespace}\nPods:\n{table}")
                logger.info(f"{message.from_user.id}: /getPods command executed")
            except client.exceptions.ApiException as e:
                self.bot.reply_to(message, f"[System] Error: {e}")
                logger.error(f"Error getting pods: {e}")

    def delete_project(self):
        @self.bot.message_handler(commands=['deleteProject'])
        def _delete_project(message):
            if not self.is_admin(message.from_user.id):
                return
            split_message = message.text.split()
            if len(split_message) < 2:
                self.bot.reply_to(message, "[System] Invalid command format. Usage: /deleteProject <project_name>")
                return
            project_name = split_message[1]
            namespace = self.namespaces.get(message.from_user.id)
            if not namespace:
                self.bot.reply_to(message, "[System] Please set the namespace first using /getK8sSettings")
                return
            config.load_kube_config()
            v1 = client.CoreV1Api()
            try:
                # Get all resources in the namespace
                pods = v1.list_namespaced_pod(namespace)
                services = v1.list_namespaced_service(namespace)
                deployments = client.AppsV1Api().list_namespaced_deployment(namespace)
                # Filter resources by project label
                project_pods = [pod for pod in pods.items if pod.metadata.labels.get('project') == project_name]
                project_services = [service for service in services.items if
                                    service.metadata.labels.get('project') == project_name]
                project_deployments = [deployment for deployment in deployments.items if
                                       deployment.metadata.labels.get('project') == project_name]
                if project_pods or project_services or project_deployments:
                    confirmation_msg = self.bot.reply_to(message,
                                                         f"[System] Are you sure you want to delete the project '{project_name}' and all related resources? (yes/no)")
                    self.bot.register_next_step_handler(confirmation_msg, self.confirm_delete_project, project_name,
                                                        namespace)
                else:
                    self.bot.reply_to(message,
                                      f"[System] Project '{project_name}' not found in namespace '{namespace}'")
            except client.exceptions.ApiException as e:
                self.bot.reply_to(message, f"[System] Error: {e}")
                logger.error(f"Error getting resources: {e}")

    def confirm_delete_project(self, message, project_name, namespace):
        if message.text.lower() == 'yes':
            config.load_kube_config()
            v1 = client.CoreV1Api()
            try:
                delete_options = client.V1DeleteOptions()
                # Get all resources in the namespace
                pods = v1.list_namespaced_pod(namespace)
                services = v1.list_namespaced_service(namespace)
                deployments = client.AppsV1Api().list_namespaced_deployment(namespace)
                # Filter resources by project label
                project_pods = [pod for pod in pods.items if pod.metadata.labels.get('project') == project_name]
                project_services = [service for service in services.items if
                                    service.metadata.labels.get('project') == project_name]
                project_deployments = [deployment for deployment in deployments.items if
                                       deployment.metadata.labels.get('project') == project_name]
                # Delete all resources related to the project
                for pod in project_pods:
                    v1.delete_namespaced_pod(name=pod.metadata.name, namespace=namespace, body=delete_options)
                for service in project_services:
                    v1.delete_namespaced_service(name=service.metadata.name, namespace=namespace, body=delete_options)
                for deployment in project_deployments:
                    client.AppsV1Api().delete_namespaced_deployment(name=deployment.metadata.name, namespace=namespace,
                                                                    body=delete_options)
                self.bot.reply_to(message,
                                  f"[System] Project '{project_name}' and all related resources have been deleted.")
                logger.info(f"{message.from_user.id}: Project '{project_name}' deleted")
            except client.exceptions.ApiException as e:
                self.bot.reply_to(message, f"[System] Error: {e}")
                logger.error(f"Error deleting project: {e}")
        else:
            self.bot.reply_to(message, "[System] Project deletion cancelled.")
            logger.info(f"{message.from_user.id}: Project deletion cancelled")

