FROM python:3.12.6-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY temp_scraper.py .
CMD ["python", "temp_scraper.py" ]