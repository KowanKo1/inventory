# Use the official Python image as a base image
FROM python:3.11.3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the current directory contents into the container at /app/
COPY . /app/

# Expose the port the app runs on
EXPOSE 8001

# Define the command to run on container start
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]