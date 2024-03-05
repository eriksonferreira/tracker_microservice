# Use a official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./app /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port available to the world outside this container
# Note: Specify the port if your application uses one, e.g., for a web server
# EXPOSE 8000

# Define environment variable for API endpoint
# Use 'host.docker.internal' to refer to the host machine in Docker for Windows/Mac.
# For Linux, you may need to use the host's IP address directly or configure the network.
ENV API_HOST=10.128.0.16

# Run main.py when the container launches
CMD ["python", "-u", "main.py"]
