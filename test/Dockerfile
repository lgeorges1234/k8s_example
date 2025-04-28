FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY ./requirements.txt /app/requirements.txt

# Copy main.py to the correct location
COPY ./app/main.py /app/main.py

# Install system dependencies
RUN apt-get update && apt-get install -y default-libmysqlclient-dev \
    build-essential \
    pkg-config

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set the PYTHONPATH to include the app directory
ENV PYTHONPATH=/app

# Command to run when container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]