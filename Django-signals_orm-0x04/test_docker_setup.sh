#!/bin/bash

echo "Testing Docker Setup for Django Messaging App"
echo "============================================="

# Check if Docker is running
echo "1. Checking Docker status..."
if docker ps > /dev/null 2>&1; then
    echo "   ✓ Docker is running"
else
    echo "   ✗ Docker is not running. Please start Docker Desktop and try again."
    exit 1
fi

# Check if Docker Compose is available
echo "2. Checking Docker Compose..."
if docker-compose --version > /dev/null 2>&1; then
    echo "   ✓ Docker Compose is available"
else
    echo "   ✗ Docker Compose is not available"
    exit 1
fi

# Build the Docker image
echo "3. Building Docker image..."
if docker build -t messaging-app .; then
    echo "   ✓ Docker image built successfully"
else
    echo "   ✗ Failed to build Docker image"
    exit 1
fi

# Test running the container
echo "4. Testing container startup..."
if docker run --rm -d --name test-messaging-app messaging-app; then
    echo "   ✓ Container started successfully"
    
    # Wait a moment for the app to start
    sleep 5
    
    # Check if container is still running
    if docker ps | grep test-messaging-app > /dev/null; then
        echo "   ✓ Container is running"
    else
        echo "   ✗ Container stopped unexpectedly"
        docker logs test-messaging-app
    fi
    
    # Clean up test container
    docker stop test-messaging-app > /dev/null 2>&1
    docker rm test-messaging-app > /dev/null 2>&1
else
    echo "   ✗ Failed to start container"
    exit 1
fi

echo ""
echo "Docker setup test completed successfully!"
echo ""
echo "Next steps:"
echo "1. Run: docker-compose up --build"
echo "2. Access the app at: http://localhost:8000"
echo "3. Check logs with: docker-compose logs"
