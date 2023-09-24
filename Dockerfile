FROM python:3.11

WORKDIR /app/

COPY . .

RUN pip install --default-timeout=60 --timeout 100 --retries 10 -r requirements.txt
