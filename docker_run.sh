#!/bin/bash


# This script is used for testing the build/deploy of a single instance of the app
# Set the port, feel free to change this
PORT=5000

# Define the Docker image name
IMAGE_NAME="basketball-stats-api"

# Check if the container is running
if docker ps -a --format "{{.Names}}" | grep -q "^${IMAGE_NAME}$"; then
    # Stop and remove the existing container
    echo "Stopping and removing existing container..."
    docker stop ${IMAGE_NAME} && docker rm ${IMAGE_NAME}
fi

# Build the Docker image
docker image build -t ${IMAGE_NAME} . --build-arg="PORT=${PORT}"

# Run the Docker container
docker run -p ${PORT}:${PORT} -d --name ${IMAGE_NAME} ${IMAGE_NAME}

echo "Application started on 127.0.0.1:${PORT}"
