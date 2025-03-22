# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port on which the Flask app will run
EXPOSE 5000

# Run the Flask application
CMD ["python", "app/app.py"]
