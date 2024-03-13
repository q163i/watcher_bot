<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/q163i/terraform-associate">
    <img src="https://avatars.githubusercontent.com/u/1525981?s=200&v=4" alt="Logo" width="80" height="80">
  </a>
  <h3 align="center">watcher-bot</h3>
  <p align="center">
    <br />
    <a href="https://github.com/q163i/watcher-bot"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/q163i/watcher-bot/issues">Report Bug</a>
    ·
    <a href="https://github.com/q163i/watcher-bot/issues">Request Feature</a>
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project
This repository contains a Telegram bot implemented in Python for IAC
- **GitOps Integration**: The bot facilitates GitOps workflows by providing essential functionalities such as network checks, SSL certificate expiration checks, and message sending directly through Telegram.
- **Infrastructure Automation**: With its ability to perform various tasks based on user commands, the bot enhances Infrastructure as Code (IAC) automation efforts. Users can trigger actions like network checks and SSL certificate validations with simple commands, reducing manual intervention.
- **Secure Communication**: The bot operates securely by requiring only the bot token and administrator user IDs for communication. This makes it suitable for deployment in closed networks or environments with restricted access.
- **Streamlined Operations**: By centralizing monitoring and management tasks within Telegram, the bot simplifies operations for DevOps teams. It provides a convenient interface for executing commands and receiving notifications, improving efficiency and collaboration.
### Deployment Flexibility
- **Server Installation**: The bot can be deployed on a server within a closed subnet, providing flexibility in deployment scenarios.
- **Minimal Configuration**: Only the Telegram bot token and administrator user IDs are required for the bot to function, minimizing setup complexity.
- **Scalability**: As a lightweight Telegram bot, it can be easily scaled up or down based on workload requirements without significant resource overhead.

<!-- Features and Usage-->
### Features
- **Network Check**: Verify the availability of a server and port by performing network checks.
- **SSL Certificate Expiration Check**: Check the expiration date of SSL certificates for specified domains.
- **Message Sending**: Send messages to authorized users via Telegram.
- **File Transfer**: Transfer files from the server to Telegram users.
- **Error Handling**: Automatically forward unauthorized or spam messages to designated users.
- **Customizable Logging**: Log messages to stdout for easy debugging and monitoring.

### Usage
1. **Network Check**: Use the `/checkNetwork` command followed by the server IP and port to check network availability.
   Example: `/checkNetwork 8.8.8.8 443`
2. **SSL Certificate Check**: Use the `/checkCertificate` command followed by the domain name to check SSL certificate expiration.
   Example: `/checkCertificate https://google.com`
3. **Message Sending**: Send messages to allowed users using the `/sendMessage` command followed by the message content.
   Example: `/sendMessage Hello, this is a test message!`
4. **File Transfer**: Run the `getData` command from the server with the `--data` flag to send a file to Telegram.
   Example: `python3 watcher_bot.py getData --data /path/to/file.txt`

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
* 0 Open console
* 1 Download Git repository:
  ```sh
  git clone https://github.com/q163i/watcher_bot.git
  ```
* 2 Go to git folder:
  ```sh
  cd watcher_bot
  ```
* 3 Look at dir files ``ls -la``:
  ```sh
  user@computername watcher_bot % ls -la
    total 64
    drwxr-xr-x  11 user  group   352 Mar 13 14:24 .
    drwxr-xr-x  12 user  group   384 Mar 13 14:22 ..
    drwxr-xr-x  14 user  group   448 Mar 13 13:53 .git
    -rw-r--r--   1 user  group    17 Mar 11 15:58 .gitignore
    drwxr-xr-x   6 user  group   192 Mar 13 13:53 Chart # Helm Charts
    -rw-r--r--   1 user  group   174 Mar 11 15:10 Dockerfile 
    -rw-r--r--@  1 user  group  5927 Mar 13 14:24 README.md
    -rw-r--r--   1 user  group   271 Mar 13 12:29 docker-compose.yml
    -rw-r--r--   1 user  group    33 Mar 13 10:55 requirements.txt 
    -rw-r--r--   1 user  group  7659 Mar 13 14:02 watcher_bot.py
  ```
* 4 Install dependencies:
  ```sh
  pip install --no-cache-dir -r requirements.txt
  ```
* 5 Export 2 keys (add in env):
  ```sh
  export TOKEN=<type_your_token>  # Specifies the Telegram bot token
  export ALLOWED_USERS=<type_admins_id>  # Specifies the allowed users for the bot
  ```
* 6 Run ``python3 watcher_bot.py``:
  ```sh
    user@computername watcher_bot % python3 watcher_bot.py                        
    2024-03-13 14:40:36,170 - INFO - [System] Daemon Started
    2024-03-13 14:40:36,346 - INFO - [System] Sending message to <your_telegram_id>: [System] Daemon Started on External IP: <your_external_ip>
  ```
#### Docker-compose (Must be install with docker)
*  1 Add(change in file) your DATA in docker-compose.yml:
  ```sh
    ***
    
    # Environment variables for configuring the bot
    environment:
      # Telegram bot token (replace with your actual token)
      - TOKEN=CHANGE_TOKEN <-----
      # Comma-separated list of allowed user IDs (replace with actual user IDs)
      - ALLOWED_USERS=CHANGE_ALLOWED_USERS <-----
     
    ***
  ```
*  2 Run ``docker-compose up``:
  ```sh
    user@computername watcher_bot % docker-compose up
    [+] Running 1/1
     ✔ Container watcher_bot                                                                                                                                          Created0.1s 
     ! python_telegram The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8) and no specific platform was requested    0.0s 
    Attaching to watcher_bot
    watcher_bot  | 2024-03-13 14:40:36,170 - INFO - [System] Daemon Started
    watcher_bot  | 2024-03-13 14:40:36,346 - INFO - [System] Sending message to <your_telegram_id>: [System] Daemon Started on External IP: <your_external_ip>
  ```
IMPORTANT: The Docker image is built for the arm/m* processor architecture.If you intend to use the image on a *nix system, please use the special build command below:
````docker build --platform linux/amd64 -t romanolitvinov/watcher_bot:latest . ````
#### Helm (must be install k8s/openshift/k3s/minikube/other)
* 1 Download your kubernetes config in env (example: k3s):
  ```sh
  export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
  ```
* 2 Create cluster (example: minikube):
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
* 3 Change default env in helm:
  ```sh
    secrets:
      TOKEN: "CHANGE_TOKEN" <---- # Specifies the Telegram bot token
      ALLOWED_USERS: "CHANGE_ALLOWED_USERS" <---- # Specifies the allowed users for the bot
  ```
* 4 Install helm Chart:
  ```sh
    user@computername watcher_bot % helm install watcher-bot ./Chart  
    NAME: watcher-bot
    LAST DEPLOYED: Wed Mar 13 15:17:48 2024
    NAMESPACE: default
    STATUS: deployed
    REVISION: 1
    TEST SUITE: None
  ```
* 5 Look at your helm charts:
  ```sh
  user@computername watcher_bot % helm list
    NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
    watcher-bot     default         1               2024-03-13 15:17:48.087093 -0400 EDT    deployed        python-0.0.1    0.0.1 
  ```
* 6 Look at your kubernetes cluster:
  ```sh
    user@computername watcher_bot % kubectl get pods
    NAME                                  READY   STATUS    RESTARTS   AGE
    watcher-bot-python-54cd7cb78b-nztbw   1/1     Running   0          11s
  
    (user@computername watcher_bot % kubectl logs watcher-bot-python-54cd7cb78b-nztbw
    2024-03-13 19:24:54,779 - INFO - [System] Bot started!
    2024-03-13 19:24:54,986 - INFO - [System] Sending message to <your_telegram_id>: [System] Daemon Started on External IP: <your_external_ip>
  ```

<!-- ROADMAP -->
## Roadmap
- [ ] Update file structure
- [ ] Add additional functionalities
- [ ] Enhance Helm chart (encrypt secrets)
- [ ] Document deployment instructions for the cloud

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
