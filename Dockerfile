FROM python:3.10.6-slim

WORKDIR '/app'

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
VOLUME /app/data


CMD [ "python", "./src/bot_telegram.py" ]