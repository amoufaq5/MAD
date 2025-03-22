# Use official Python base image
FROM python:3.9-slim

# Create app directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Expose Flask port
EXPOSE 5000

CMD ["python", "app/app.py"]
