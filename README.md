<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/q163i/watcher_bot">
  </a>
  <h3 align="center">watcher_bot</h3>
    <div align="center">
      <img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExeTFrdWR4amdsdHUzYXdkc2puZXBsdThuc2J1a21jdm50aTA4eTZmbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/2WGDUTmsB4DzFuvZ2t/giphy.gif" alt="Example GIF">
    </div>
  <p align="center">
    <br />
    <a href="https://github.com/q163i/watcher_bot"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/q163i/watcher_bot/issues">Report Bug</a>
    ·
    <a href="https://github.com/q163i/watcher_bot/issues">Request Feature</a>
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project
This repository contains a Telegram bot implemented in Python for IAC
- **GitOps Integration**: The bot facilitates GitOps workflows by providing essential functionalities such as network checks, SSL certificate expiration checks, and message sending directly through Telegram.
- **Infrastructure Automation**: With its ability to perform various tasks based on user commands, the bot enhances Infrastructure as Code (IAC) automation efforts. Users can trigger actions like network checks and SSL certificate validations with simple commands, reducing manual intervention.
- **Secure Communication**: The bot operates securely by requiring only the bot token and administrator user IDs for communication. This makes it suitable for deployment in closed networks or environments with restricted access.
- **Streamlined Operations**: By centralizing monitoring and management tasks within Telegram, the bot simplifies operations for DevOps teams. It provides a convenient interface for executing commands and receiving notifications, improving efficiency and collaboration.
- **Project Deletion**: The bot now supports the deletion of all resources related to a specific project in a Kubernetes namespace. This is done through the `/deleteProject <project_name>` command.
### Deployment Flexibility
- **Server Installation**: The bot can be deployed on a server within a closed subnet, providing flexibility in deployment scenarios.
- **Minimal Configuration**: Only the Telegram bot token and administrator user IDs are required for the bot to function, minimizing setup complexity.
- **Scalability**: As a lightweight Telegram bot, it can be easily scaled up or down based on workload requirements without significant resource overhead.
- **Dashboard Integration**: The bot now includes Flask, enabling the use of a dashboard for managing bot functionalities and monitoring activities.
- **Kubernetes Integration**: The bot can interact with a Kubernetes cluster using the Kubernetes API. This allows the bot to perform various tasks such as retrieving the list of running pods, checking the status of deployments, and more. Before the bot can interact with your Kubernetes cluster, you need to create a ServiceAccount in Kubernetes. This ServiceAccount will be used by the bot to authenticate with the Kubernetes API.

<!-- Additional Features and Usage-->
### Additional Features
- **Disk Space Check**: Use the `/checkDiskSpace` command to check the disk space usage on the server.
- **CPU Usage Check**: Use the `/checkCPUUsage` command to check the CPU usage on the server.
- **Memory Usage Check**: Use the `/checkMemoryUsage` command to check the memory usage on the server.
- **Project Deletion (only with k8s)**: Use the `/deleteProject <project_name>` command to delete all resources related to a specific project in a Kubernetes namespace.

### Database Information
This project utilizes a NoSQL database for efficient and flexible data storage. NoSQL databases are particularly beneficial for this project due to their inherent scalability and adaptability. The bot performs various database operations using the NoSQL database, including creating, reading, updating, and deleting data as required for its functionalities. The NoSQL database used in this project also ensures data security with its built-in security features, such as access controls, encryption, and backups for data protection. Please replace this template information with specifics about the NoSQL database you are using in your project, such as the type of NoSQL database (Document, Key-Value, Column, Graph), the specific NoSQL database system (MongoDB, CouchDB, Cassandra, etc.), and how it is used in your project.

### Automated Tests
This project uses automated tests to ensure the security of the web server. These tests are written using the `pytest` and `requests` libraries and check the following aspects:

- Enabling of the modern and secure TLSv1.2 protocol (`test_tlsv1_2_enabled`)

The tests are located in the `tests/test_security.py` file.

To run the tests, use the following command:

```sh
pytest bot/tests/HttpSecurityTests.py
```

<!-- GETTING STARTED -->
### Pre-Install
This is an example of how to list things you need to use the software and how to install them.

The next steps for macOS
* Install HomeBrew
* Open console in apps and type command
```sh 
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
* Install k8s-cli (if kubernetes)
```sh
brew install kubernetes-cli
```
* Install helm (if kubernetes)
```sh
brew install helm
```

<!-- Installation -->
### Installation
#### Python (must be install with git)
* Open console
* Download Git repository:
```sh
git clone https://github.com/q163i/watcher_bot.git
```
* Go to git folder:
```sh
cd watcher_bot
```
* Look at dir files ``ls -la``:
```sh
user@computername watcher_bot % ls -la
total 64
drwxr-xr-x  11 user  group   352 Mar 1 01:00 .
drwxr-xr-x  12 user  group   384 Mar 1 01:00 ..
drwxr-xr-x  14 user  group   448 Mar 1 01:00 .git
-rw-r--r--   1 user  group    17 Mar 1 01:00 .gitignore
drwxr-xr-x   6 user  group   192 Mar 1 01:00 Chart # Helm Charts
-rw-r--r--   1 user  group   174 Mar 1 01:00 Dockerfile 
-rw-r--r--@  1 user  group  5927 Mar 1 01:00 README.md
drwxr-xr-x   5 user  group   160 Mar 1 01:00 bot
-rw-r--r--   1 user  group   271 Mar 1 01:00 docker-compose.yml
-rw-r--r--   1 user  group   116 Mar 1 01:00 requirements.txt
-rw-r--r--   1 user  group   116 Mar 1 01:00 secret_validator.py # Check your secrets (pre-commit)

```
* Install dependencies:
```sh
pip install --no-cache-dir -r ./bot/requirements.txt
```
* Export 2 keys (add in env):
```sh
export TOKEN=<type_your_token>  # Specifies the Telegram bot token
export ALLOWED_USERS=<type_admins_id>  # Specifies the allowed users for the bot
# If you work with k8s
export KUBERNETES_API_URL=<type_k8s_url>  # Specifies the Kubernetes API URL
export KUBERNETES_TOKEN=<type_k8s_token>  # Specifies the Kubernetes API token
```
* Run ``python3 watcher_bot.py``:
```sh
user@computername watcher_bot % python3 watcher_bot.py                        
2024-03-13 14:40:36,170 - INFO - [System] Daemon Started
2024-03-13 14:40:36,346 - INFO - [System] Sending message to <your_telegram_id>: [System] Daemon Started on External IP: <your_external_ip>
```
#### Docker-compose (Must be install with docker)
*  Add(change in file) your DATA in docker-compose.yml:
```sh
***
# Environment variables for configuring the bot
environment:
  # Telegram bot token (replace with your actual token)
  - TOKEN=CHANGE_TOKEN <-----
  # Comma-separated list of allowed user IDs (replace with actual user IDs)
  - ALLOWED_USERS=CHANGE_ALLOWED_USERS <-----
  # If you work with k8s
  # Kubernetes API URL (replace with actual URL)
  - KUBERNETES_API_URL=CHANGE_K8S_URL <-----
  # Kubernetes API token (replace with actual token)
  - KUBERNETES_API_TOKEN=CHANGE_TOKEN <----- 
***
```
*  Run ``docker-compose up``:
```sh
user@computername watcher_bot % docker-compose up

[+] Running 1/1
 ✔ Container watcher_bot                                                                                                                                          Created0.1s 
 ! watcher_bot The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8) and no specific platform was requested    0.0s 
Attaching to watcher_bot
watcher_bot  | 2024-03-13 14:40:36,170 - INFO - [System] Daemon Started
watcher_bot  | 2024-03-13 14:40:36,346 - INFO - [System] Sending message to <your_telegram_id>: [System] Daemon Started on External IP: <your_external_ip>
```

IMPORTANT: Docker build for amd/arm platform with buildx:
````
docker buildx create --name=container --driver=docker-container --use --bootstrap

docker buildx build \
  --builder=container \
  --platform=linux/amd64,linux/arm64 \
  -t romanolitvinov/watcher_bot:latest \
  --push .
````

#### Helm (must be install k8s/openshift/k3s/minikube/other)
* Download your kubernetes config in env (example: k3s):
```sh
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
```
* Create cluster (example: minikube):
```sh
user@computername watcher_bot % minikube start 
😄  minikube v1.32.0 on Darwin 14.4 (arm64)
✨  Automatically selected the docker driver
📌  Using Docker Desktop driver with root privileges
👍  Starting control plane node minikube in cluster minikube
🚜  Pulling base image ...
🔥  Creating docker container (CPUs=2, Memory=2200MB) ...
🐳  Preparing Kubernetes v1.28.3 on Docker 24.0.7 ...
    ▪ Generating certificates and keys ...
    ▪ Booting up control plane ...
    ▪ Configuring RBAC rules ...
🔗  Configuring bridge CNI (Container Networking Interface) ...
🔎  Verifying Kubernetes components...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
🌟  Enabled addons: storage-provisioner, default-storageclass
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```
* Change default env in helm:
```sh
secrets:
  TOKEN: "CHANGE_TOKEN" <---- # Specifies the Telegram bot token
  ALLOWED_USERS: "CHANGE_ALLOWED_USERS" <---- # Specifies the allowed users for the bot
```
* If you use sops, you can encrypt your secrets:
```sh
# Install sops
brew install sops
brew install gnupg

# Add variables
export KEY_NAME="My Key"
export KEY_EMAIL='my@mail.com'
export KEY_COMMENT="Private key for my!"
export YOUR_PASSPHRASE='<the_passphrase>'

# Generate GPG key
gpg --batch --full-generate-key <<EOF
%no-protection
Key-Type: 1
Key-Length: 4096
Subkey-Type: 1
Subkey-Length: 4096
Expire-Date: 0
Name-Comment: ${KEY_COMMENT}
Name-Real: ${KEY_NAME}
Name-Email: ${KEY_EMAIL}
Passphrase: ${YOUR_PASSPHRASE}
EOF

key_gpg=$(gpg --list-keys | grep -A 1 pub | grep '^      CDC' | awk '{print $1}')
echo "creation_rules:
    - pgp: >-
        $key_gpg" > Chart/.sops.yaml

# Encrypt secrets
helm secrets encrypt Chart/secrets.yaml.dec > Chart/secrets.yaml

# After work - decrypt secrets
helm secrets decrypt Chart/secrets.yaml > Chart/secrets.yaml.dec
````

* Installation helm Chart:
```sh
user@computername watcher_bot % helm upgrade \
  --atomic \
  --cleanup-on-fail \
  --install watcher-bot ./Chart \
  -f Chart/values.yaml \
  --namespace default \
  --wait --timeout 300
#    -f Chart/secrets.yaml \
#  --set image.tag=latest \

NAME: watcher-bot
LAST DEPLOYED: Wed Mar 13 15:17:48 2024
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
```
* Look at your helm charts:
```sh
user@computername watcher_bot % helm list

NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
watcher-bot     default         1               2024-03-13 15:17:48.087093 -0400 EDT    deployed        python-0.0.1    0.0.1 
```
* Look at your kubernetes cluster:
```sh
user@computername watcher_bot % kubectl get pods

NAME                                  READY   STATUS    RESTARTS   AGE
watcher-bot-python-54cd7cb78b-nztbw   1/1     Running   0          11s

(user@computername watcher_bot % kubectl logs watcher-bot-python-54cd7cb78b-nztbw
2024-03-13 19:24:54,779 - INFO - [System] Bot started!
2024-03-13 19:24:54,986 - INFO - [System] Sending message to <your_telegram_id>: [System] Daemon Started on External IP: <your_external_ip>
```

## Run without Daemon mode (information about deployment)
Example commands:
```sh
# DO NOT FORGET ABOUT ENV VARIABLES
# TOKEN=<type_your_token> ALLOWED_USERS=<type_admins_id>

python3 ./bot/SimpleMessage.py infoDeploySuccess --text "Deployment was successful"
python3 ./bot/SimpleMessage.py infoDeployFail --text "Deployment failed"
python3 ./bot/SimpleMessage.py sendFileToUser --path "<path>"
```

### Capabilities

- **Command Line Arguments**: The script accepts command line arguments to specify the command to execute (`infoDeploySuccess` or `infoDeployFail`), the ID of the admin chat, and the text to send.

- **Deployment Status Messages**: The script can send two types of deployment status messages: `infoDeploySuccess` and `infoDeployFail`. These messages can be customized with the `--text` command line argument.

- **Environment Variable Substitution**: The script supports environment variable substitution in the text messages. This allows you to include dynamic information in your messages. For example, you can include the deployment stage, project name, version, and error message in your deployment status messages.

- **Error Handling**: The script includes error handling to ensure that it fails gracefully if an error occurs. For example, it checks that the Telegram bot token and allowed users are set, and it catches exceptions when sending messages.

To use the script, you can run it from the command line with the appropriate arguments. For example:

```sh
python3 ./bot/SimpleMessage.py infoDeploySuccess --adminChat $ALLOWED_USERS --text "Deployment was successful"
```
This will send a message to the specified admin chat indicating that the deployment was successful. Please replace the command and text with the actual command and message you want to send.

## Deploy to the cloud (pythonanywhere.com)
Sure, here's a step-by-step guide on how to deploy your project on PythonAnywhere:

1. **Create an account on PythonAnywhere**: If you don't have an account yet, go to [PythonAnywhere](https://www.pythonanywhere.com) and sign up for a new account.

2. **Open the PythonAnywhere dashboard**: After logging in, you'll be taken to your dashboard. Click on the "Web" tab.

3. **Add a new web app**: Click on the "Add a new web app" button. Follow the steps in the wizard. When asked for the Python version, choose the one that matches your project.

4. **Configure the WSGI file**: PythonAnywhere uses the WSGI standard for Python web apps. You'll need to edit the WSGI configuration file to point PythonAnywhere at your web app. The path to this file is displayed on the "Web" tab. It's usually in the format `/var/www/your_username_pythonanywhere_com_wsgi.py`.

5. **Upload your code**: You can upload your code to PythonAnywhere using Git. First, install Git on PythonAnywhere using the "Bash" console with the command `git clone https://github.com/q163i/watcher_bot.git`. Then, navigate to the directory where you want to put your code, and clone your repository.

6. **Install dependencies**: If your project has any dependencies listed in a `requirements.txt` file, you can install them using pip. Open a Bash console, navigate to your project's directory, and run `pip install --user -r requirements.txt`.

7. **Reload your web app**: After you've uploaded your code and installed your dependencies, go back to the "Web" tab and hit the "Reload" button. PythonAnywhere will restart your web app with the new code.

8. **Check your site**: You should now be able to visit your username.pythonanywhere.com and see your web app live!

Remember to replace `your_username` with your actual PythonAnywhere username and `https://github.com/q163i/watcher_bot.git` with the actual URL of your Git repository.

<!-- ROADMAP -->
## Roadmap
- [X] The file structure has been updated.
- [X] Additional functionalities have been added.
- [X] The Helm chart has been enhanced with encrypted secrets.
- [X] Deployment instructions for the cloud have been documented
- [X] Add ingress settings
- [X] Add/uncomment Probes (50%)
- [X] k8s integration
- [X] Add SimpleMessage.py - for deployment status messages and send files
- [ ] Add flask for production work

<!-- CONTRIBUTING -->
## Contributing
See the [open issues](https://github.com/q163i/watcher_bot/issues) for a full list of proposed features (and known issues).

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## License
Distributed under the MIT License.

<!-- CONTACT -->
## Contact
Roman Litvinov - https://q163i.github.io
Project Link: [https://github.com/q163i/watcher_bot](https://github.com/q163i/watcher_bot)
