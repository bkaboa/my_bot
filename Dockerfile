FROM python:3.13.0

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir discord.py

CMD ["python3", "client.py"]