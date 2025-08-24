#!/bin/bash

# Jenkins Setup Script for Django Messaging App
# This script helps set up Jenkins and configure the pipeline

echo "🚀 Setting up Jenkins for Django Messaging App..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if Jenkins container already exists
if docker ps -a --format 'table {{.Names}}' | grep -q "jenkins"; then
    echo "⚠️  Jenkins container already exists. Removing it..."
    docker stop jenkins
    docker rm jenkins
fi

# Check if Jenkins volume exists
if docker volume ls --format 'table {{.Name}}' | grep -q "jenkins_home"; then
    echo "⚠️  Jenkins volume already exists. Removing it..."
    docker volume rm jenkins_home
fi

echo "📦 Pulling Jenkins LTS image..."
docker pull jenkins/jenkins:lts

echo "🔧 Creating Jenkins container..."
docker run -d \
    --name jenkins \
    -p 8080:8080 \
    -p 50000:50000 \
    -v jenkins_home:/var/jenkins_home \
    -v /var/run/docker.sock:/var/run/docker.sock \
    jenkins/jenkins:lts

echo "⏳ Waiting for Jenkins to start..."
sleep 30

# Get initial admin password
echo "🔑 Getting initial admin password..."
INITIAL_PASSWORD=$(docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword 2>/dev/null || echo "Password not available yet")

if [ "$INITIAL_PASSWORD" != "Password not available yet" ]; then
    echo "✅ Jenkins is ready!"
    echo "🌐 Access Jenkins at: http://localhost:8080"
    echo "🔑 Initial admin password: $INITIAL_PASSWORD"
    echo ""
    echo "📋 Next steps:"
    echo "1. Open http://localhost:8080 in your browser"
    echo "2. Install suggested plugins (including Git, Pipeline, and ShiningPanda)"
    echo "3. Create admin user"
    echo "4. Create new pipeline job"
    echo "5. Configure GitHub credentials"
    echo "6. Set up Docker Hub credentials"
    echo ""
    echo "🔧 Required Jenkins plugins:"
    echo "- Git plugin"
    echo "- Pipeline plugin"
    echo "- ShiningPanda plugin"
    echo "- Docker plugin"
    echo "- Credentials plugin"
    echo "- HTML Publisher plugin"
    echo "- Cobertura plugin"
else
    echo "⏳ Jenkins is still starting up. Please wait a few more minutes and check:"
    echo "docker logs jenkins"
fi

echo ""
echo "📚 Useful commands:"
echo "  View logs: docker logs jenkins"
echo "  Stop Jenkins: docker stop jenkins"
echo "  Start Jenkins: docker start jenkins"
echo "  Restart Jenkins: docker restart jenkins"
echo "  Remove Jenkins: docker rm -f jenkins && docker volume rm jenkins_home"
