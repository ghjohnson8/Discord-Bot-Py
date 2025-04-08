# Use the official Python image as a base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Ensure DNS resolution works by using Cloudflare's DNS
RUN echo "nameserver 1.1.1.1" > /etc/resolv.conf && \
    echo "nameserver 1.0.0.1" >> /etc/resolv.conf

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libffi-dev \
    python3-dev \
    build-essential \
    iputils-ping

# Copy the rest of the application files into the container
COPY . /app/

# Set environment variables from the .env file (optional)
COPY .env /app/.env

# Run the bot when the container starts
CMD ["python", "-u", "bot.py"]