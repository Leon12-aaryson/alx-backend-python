# 🚀 Quick Start Guide

## ⚡ Get Jenkins Running in 5 Minutes

### 1. Start Docker
```bash
# Make sure Docker Desktop is running
# Or start Docker service if on Linux
```

### 2. Run Jenkins Setup
```bash
cd messaging_app
./setup_jenkins.sh
```

### 3. Access Jenkins
- Open: http://localhost:8080
- Password: Check terminal output or run:
  ```bash
  docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
  ```

### 4. Install Plugins
Choose "Install suggested plugins" - this includes:
- ✅ Git plugin
- ✅ Pipeline plugin  
- ✅ ShiningPanda plugin

### 5. Create Pipeline Job
1. **New Item** → **Pipeline**
2. **Pipeline script from SCM**
3. **Git** + Your repo URL
4. **Script Path**: `messaging_app/Jenkinsfile`

## 🔑 Required Credentials

### GitHub Credentials
- Username + Password or SSH key
- For accessing your repository

### Docker Hub Credentials  
- ID: `docker-hub-credentials`
- Username + Access Token
- For pushing Docker images

## 🧪 Test Everything

### Local Testing
```bash
./run_tests.sh
```

### Jenkins Testing
1. Click **Build Now**
2. Watch the pipeline run
3. Check generated reports

## 📊 What You'll Get

- ✅ Automated testing on every commit
- ✅ Code quality checks with flake8
- ✅ Test coverage reports
- ✅ Docker image building
- ✅ Automatic deployment preparation
- ✅ GitHub Actions integration

## 🆘 Need Help?

- **Setup Issues**: Check `JENKINS_SETUP.md`
- **Validation**: Run `./validate_setup.sh`
- **Testing**: Run `./run_tests.sh`
- **Documentation**: See `SETUP_SUMMARY.md`

---

**🎯 Goal**: Get Jenkins running and pipeline working in under 10 minutes!
