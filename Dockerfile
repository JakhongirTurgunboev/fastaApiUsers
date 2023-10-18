# Use the official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Install the Alembic library
RUN pip install alembic

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run Alembic migrations before starting the application
CMD ["alembic", "upgrade", "head", "&&", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

# Run main.py when the container launches
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
