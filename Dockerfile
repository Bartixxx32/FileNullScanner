# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any Python dependencies if you have a requirements.txt file
# RUN pip install -r requirements.txt  # Uncomment if needed

# Set the entrypoint for the container to run the Python script
ENTRYPOINT ["python", "scanner.py"]
