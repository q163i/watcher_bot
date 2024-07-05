# Description: Dockerfile for the watcher_bot
FROM python:alpine

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the local directory's contents into the container at /app
COPY . .

# Install Python dependencies from requirements.txt without caching
RUN pip install -r requirements.txt --no-cache-dir

# Create a non-root user
RUN addgroup --gid 1001 user && \
    adduser -u 1001 -G user -D -H user

# Switch to the non-root user
USER user

# Set the HEALTHCHECK instruction to monitor the container
#HEALTHCHECK --interval=10s --timeout=5s --retries=3 CMD ps aux | grep main.py | grep -v grep

# Command to run the application when the container starts
CMD ["python", "bot/main.py"]
