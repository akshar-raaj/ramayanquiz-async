# Use an official Python image as a base
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# CMD Array form for flexibility, instead of exec form
# Run Python in unbuffered mode, to ensure print happens to stdout immediately
# instead of buffered fashion.
CMD ["python", "-u", "receive.py"]
