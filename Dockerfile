FROM python:alpine

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY watcher_bot.py .

CMD [ "python", "/app/watcher_bot.py" ]
