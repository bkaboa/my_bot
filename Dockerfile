FROM python:3.13.0

WORKDIR /app
COPY . .

ARG DISCORD_TOKEN
ENV DISCORD_TOKEN=${DISCORD_TOKEN}

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "client.py"]