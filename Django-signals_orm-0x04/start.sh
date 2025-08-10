#!/bin/bash

echo "Starting Django Messaging App with Docker Compose"
echo "================================================"

# Check if Docker is running
if ! docker ps > /dev/null 2>&1; then
    echo "Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found. Please create it with your environment variables."
    exit 1
fi

echo "Building and starting services..."
echo ""

# Build and start services
docker-compose up --build

echo ""
echo "Services stopped."
echo "To run in background, use: docker-compose up -d --build"
echo "To view logs: docker-compose logs -f"
echo "To stop services: docker-compose down"
