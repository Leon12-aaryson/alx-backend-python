# Jenkins and GitHub Actions Setup Guide

This guide will help you set up Jenkins and GitHub Actions for your Django messaging app.

## 🚀 Quick Start

### 1. Install Jenkins

Run the setup script:
```bash
chmod +x setup_jenkins.sh
./setup_jenkins.sh
```

Or manually run:
```bash
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts
```

### 2. Access Jenkins
- Open http://localhost:8080 in your browser
- Get initial password: `docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword`
- Follow setup wizard

## 🔧 Jenkins Configuration

### Required Plugins
Install these plugins in Jenkins:
- **Git plugin** - For source code management
- **Pipeline plugin** - For pipeline as code
- **ShiningPanda plugin** - For Python support
- **Docker plugin** - For building Docker images
- **Credentials plugin** - For storing secrets
- **HTML Publisher plugin** - For test reports
- **Cobertura plugin** - For coverage reports

### Credentials Setup

#### GitHub Credentials
1. Go to **Manage Jenkins** → **Manage Credentials**
2. Click **Global** → **Add Credentials**
3. Choose **SSH Username with private key** or **Username with password**
4. Add your GitHub credentials

#### Docker Hub Credentials
1. Go to **Manage Jenkins** → **Manage Credentials**
2. Click **Global** → **Add Credentials**
3. Choose **Username with password**
4. ID: `docker-hub-credentials`
5. Username: Your Docker Hub username
6. Password: Your Docker Hub access token

### Pipeline Configuration
1. Create **New Item** → **Pipeline**
2. Configure **Pipeline script from SCM**
3. SCM: **Git**
4. Repository URL: Your GitHub repo URL
5. Credentials: Select your GitHub credentials
6. Branch: `*/main` or `*/master`
7. Script Path: `messaging_app/Jenkinsfile`

## 📋 GitHub Actions Setup

### Repository Secrets
Add these secrets in your GitHub repository:
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add:
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub access token

### Workflows
Two workflows are configured:
- **`.github/workflows/ci.yml`** - Runs tests and code quality checks
- **`.github/workflows/dep.yml`** - Builds and pushes Docker images

## 🧪 Testing Configuration

### Pytest Configuration
- `pytest.ini` - Configures pytest for Django
- `.flake8` - Code quality rules
- Coverage reports generated automatically

### Running Tests Locally
```bash
# Install test dependencies
pip install pytest pytest-django pytest-cov flake8

# Run tests with coverage
pytest --cov=chats --cov-report=html

# Run code quality checks
flake8 .
```

## 🐳 Docker Configuration

### Jenkinsfile Stages
1. **Checkout** - Pull source code
2. **Install Dependencies** - Install Python packages
3. **Code Quality Check** - Run flake8
4. **Run Tests** - Execute pytest with coverage
5. **Build Docker Image** - Build Docker image
6. **Push Docker Image** - Push to Docker Hub

### Docker Image
- Base: `python:3.10-slim`
- Exposes port 8000
- Uses Gunicorn for production

## 📊 Reports and Artifacts

### Jenkins Reports
- **Coverage Report**: HTML coverage report
- **Test Results**: JUnit XML test results
- **Build History**: Complete build logs

### GitHub Actions Artifacts
- **Coverage Reports**: HTML and XML coverage
- **Test Results**: Coverage data files

## 🔍 Troubleshooting

### Common Issues

#### Jenkins Container Issues
```bash
# Check logs
docker logs jenkins

# Restart container
docker restart jenkins

# Check container status
docker ps -a | grep jenkins
```

#### Pipeline Failures
- Check build logs in Jenkins
- Verify credentials are correct
- Ensure Docker daemon is accessible
- Check GitHub repository permissions

#### Test Failures
- Verify Django settings
- Check database connectivity
- Ensure all dependencies are installed

### Useful Commands
```bash
# View Jenkins logs
docker logs -f jenkins

# Access Jenkins container
docker exec -it jenkins bash

# Check Jenkins status
docker exec jenkins systemctl status jenkins

# Backup Jenkins data
docker run --rm -v jenkins_home:/data -v $(pwd):/backup alpine tar czf /backup/jenkins_backup.tar.gz -C /data .
```

## 📚 Additional Resources

- [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Pytest Documentation](https://docs.pytest.org/)

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review Jenkins and GitHub Actions logs
3. Verify all credentials and permissions
4. Ensure Docker and required services are running
