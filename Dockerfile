# Use the Python Alpine image as the base image
FROM python:alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt ./

# Install the Python dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script to the working directory
COPY watcher_bot.py .

# Specify the command to run when the container starts
CMD [ "python", "/app/watcher_bot.py" ]
