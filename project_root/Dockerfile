# Use an official Python image as a base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Set up a working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container
COPY . .

# Expose any necessary ports (for example, if the pipeline serves a web service)
# EXPOSE 8080

# Set the default command to run the main pipeline
CMD ["python", "main_pipeline.py"]
