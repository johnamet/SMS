# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
# Install dependencies
RUN pip install --no-cache-dir --upgrade pip 
# Copy the rest of the application code
COPY . /app/

# Set environment variables for your application
ENV STORAGE_ENGINE=db
ENV STORAGE_USER=test_sms
ENV STORAGE_PASSWORD=test_sms_password
ENV STORAGE_DATABASE=sms_test_db
ENV STORAGE_HOST=localhost

# Expose the port your app runs on
EXPOSE 8080

# Command to run your application
CMD ["python3", "-m", "modules.service.v1.app"]

