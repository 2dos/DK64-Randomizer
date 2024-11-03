# Use the official Python slim image as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app
# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN apt-get update && apt-get install xdelta3 -y && pip install pyxdelta && \
    apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    make \
    xdelta3 \
    git \
    build-essential \
    && pip install -r requirements.txt \
    && pip install -r requirements-dev.txt

# Make ports 5000 and 8000 available to the world outside this container
EXPOSE 5000
EXPOSE 8000

# Run runner.py when the container launches
CMD ["python", "./runner.py"]