FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Use the startup script instead of launching uvicorn directly
CMD ["python", "start.py"]