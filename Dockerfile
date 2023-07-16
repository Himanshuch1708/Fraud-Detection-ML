# Use an official Python runtime as the base image
FROM python:3.8-slim-buster

# Install libpq-dev
RUN apt-get update && apt-get install -y libpq-dev

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files to the container
COPY . .

# Set the command to run when the container starts
CMD [ "python", "app.py" ]
