FROM python:3.11

COPY . .

RUN pip install --default-timeout=60 --timeout 100 --retries 10 --no-cache-dir -r requirements.txt

EXPOSE 8000

