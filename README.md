# AI Medical Diagnostic System MVP

This project is an advanced AI system designed to diagnose medical cases using a multimodal approach (text, images, blood tests). It scrapes data from multiple sources, trains a TensorFlow model, and serves predictions via a Flask API. The system is containerized using Docker for production-level deployment.

## Project Structure
- **data_scraping/**: Contains modules for scraping websites and APIs.
- **data/**: Stores raw scraped data.
- **models/**: Contains model definitions and training scripts.
- **app/**: Flask API for serving the model.
- **Dockerfile**: Docker configuration for containerization.
- **requirements.txt**: Python dependencies.

## Step-by-Step Guide

1. **Clone the Repository:**
