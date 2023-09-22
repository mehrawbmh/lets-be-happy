FROM python:3.11

RUN mkdir -p /usr/app/
WORKDIR /app/

COPY . .

RUN pip install --default-timeout=60 --timeout 100 --retries 10 -r requirements.txt

EXPOSE 8000

