# Use an official Python image as a base
FROM python:3.10-slim

# Install ps
RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Add Healthcheck
HEALTHCHECK CMD ps -C python || exit 1

# CMD Array form for flexibility, instead of exec form
# Run Python in unbuffered mode, to ensure print happens to stdout immediately
# instead of buffered fashion.
CMD ["python", "-u", "receive.py"]
