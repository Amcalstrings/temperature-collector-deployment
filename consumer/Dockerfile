FROM python:3.12.6-slim

WORKDIR /app

# Install system dependencies required for psycopg2
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY kafka_consumer.py .

CMD ["python", "kafka_consumer.py"]
