# 🚀 Jenkins Local Setup Guide

This guide will help you set up and test the API Automation Framework using Jenkins locally.

## 📋 Prerequisites

### Required Software
- **Java 8 or higher** (for Jenkins)
- **Python 3.8+** (for test execution)
- **Git** (for repository access)
- **Jenkins** (LTS version recommended)

### System Requirements
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Disk Space**: At least 2GB free space
- **OS**: Windows, Linux, or macOS

## 🔧 Jenkins Installation

### Windows Installation
1. **Download Jenkins**
   ```bash
   # Download Jenkins LTS from: https://jenkins.io/download/
   # Or use Chocolatey:
   choco install jenkins-lts
   ```

2. **Start Jenkins Service**
   ```bash
   # Start as Windows Service
   net start jenkins
   
   # Or run manually
   java -jar jenkins.war
   ```

3. **Access Jenkins**
   - Open browser: `http://localhost:8081`
   - Get initial admin password from: `C:\Program Files\Jenkins\secrets\initialAdminPassword`

### Linux Installation
```bash
# Ubuntu/Debian
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt-get update
sudo apt-get install jenkins

# Start Jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

### macOS Installation
```bash
# Using Homebrew
brew install jenkins-lts

# Start Jenkins
brew services start jenkins-lts
```

## ⚙️ Jenkins Configuration

### 1. Initial Setup
1. **Unlock Jenkins**
   - Access `http://localhost:8080`
   - Enter initial admin password
   - Install suggested plugins

2. **Create Admin User**
   - Username: `admin`
   - Password: `admin123` (or your preferred password)
   - Email: `admin@localhost`

### 2. Install Required Plugins
Go to **Manage Jenkins > Manage Plugins > Available** and install:

#### Essential Plugins
- ✅ **Git plugin** - Git integration
- ✅ **Pipeline** - Pipeline support
- ✅ **Credentials Binding** - Secure credential management
- ✅ **HTML Publisher** - HTML report publishing
- ✅ **Cobertura** - Coverage reporting
- ✅ **JUnit** - Test result processing

#### Optional Plugins
- ✅ **Blue Ocean** - Modern UI for pipelines
- ✅ **Timestamper** - Build timestamps
- ✅ **Workspace Cleanup** - Clean workspace after builds

### 3. Configure Global Tools
Go to **Manage Jenkins > Global Tool Configuration**:

#### Python Configuration
- **Name**: `Python3`
- **Installation**: 
  - **Install automatically**: ✅
  - **Install from**: `python.org`
  - **Version**: `3.11.0` (or latest stable)

#### Git Configuration
- **Name**: `Default`
- **Installation**: 
  - **Install automatically**: ✅
  - **Install from**: `git-scm.com`

## 🔐 GitHub Token Configuration

### 1. Add GitHub Credentials
1. Go to **Manage Jenkins > Manage Credentials**
2. Click **System > Global credentials > Add Credentials**
3. Configure:
   ```
   Kind: Username with password
   Scope: Global
       Username: joacolabrisca
    Password: YOUR_GITHUB_TOKEN_HERE
    ID: github-token
   Description: GitHub Personal Access Token
   ```

### 2. Alternative: SSH Key Setup
If you prefer SSH authentication:

1. **Generate SSH Key** (if not exists):
   ```bash
   ssh-keygen -t rsa -b 4096 -C "joacolabrisca@gmail.com"
   ```

2. **Add to GitHub**:
   - Copy public key: `cat ~/.ssh/id_rsa.pub`
   - Add to GitHub: Settings > SSH and GPG keys

3. **Add to Jenkins**:
   ```
   Kind: SSH Username with private key
   Username: git
   Private Key: From file on Jenkins master
   ```

## 🏗️ Create Jenkins Pipeline Job

### 1. Create New Pipeline
1. **Dashboard > New Item**
2. **Name**: `API-Automation-Framework`
3. **Type**: Pipeline
4. **Click OK**

### 2. Configure Pipeline
1. **General Settings**:
   - ✅ **Discard old builds**
   - **Days to keep builds**: `7`
   - **Max # of builds to keep**: `10`

2. **Build Triggers**:
   - ✅ **Poll SCM**
   - **Schedule**: `H/5 * * * *` (every 5 minutes)

3. **Pipeline Definition**:
   - **Definition**: Pipeline script from SCM
   - **SCM**: Git
   - **Repository URL**: `https://github.com/joacolabrisca/avenga_challenge_solution.git`
   - **Credentials**: Select your GitHub token
   - **Branch Specifier**: `*/master`
   - **Script Path**: `Jenkinsfile`

### 3. Advanced Pipeline Configuration
```groovy
// Optional: Add environment variables
pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.11'
        VENV_NAME = 'venv'
        REPORTS_DIR = 'reports'
    }
    
    stages {
        // ... existing stages from Jenkinsfile
    }
}
```

## 🧪 Test the Pipeline

### 1. Manual Build
1. **Click "Build Now"**
2. **Monitor build progress**
3. **Check console output**

### 2. Expected Build Stages
```
✅ Checkout
✅ Setup Environment  
✅ Install Dependencies
✅ Code Quality
✅ Run Tests
✅ Generate Reports
✅ Archive Reports
```

### 3. Build Artifacts
After successful build, you should see:
- **HTML Report**: `reports/report.html`
- **Coverage Report**: `reports/coverage/index.html`
- **JSON Report**: `reports/report.json`

### Debug Commands
```bash
# Check Jenkins logs
tail -f /var/log/jenkins/jenkins.log

# Check workspace
ls -la /var/lib/jenkins/workspace/

# Test Python installation
python3 --version
pip3 --version
```

## 📊 Monitoring and Reports

### 1. Build History
- **Dashboard**: View all builds
- **Trends**: Success/failure rates
- **Duration**: Build time analysis

### 2. Test Reports
- **HTML Reports**: Interactive test results
- **Coverage**: Code coverage metrics
- **Trends**: Test result history

### 3. Pipeline Visualization
- **Blue Ocean**: Modern pipeline view
- **Stage View**: Traditional stage view
- **Console Output**: Detailed logs

## 🔄 Continuous Integration

### 1. Webhook Setup (Optional)
For automatic builds on push:

1. **GitHub Repository Settings**
   - Webhooks > Add webhook
   - Payload URL: `http://your-jenkins-url/github-webhook/`
   - Content type: `application/json`
   - Events: `Just the push event`

2. **Jenkins Configuration**
   - Build Triggers: ✅ **GitHub hook trigger for GITScm polling**

### 2. Scheduled Builds
```groovy
// In Jenkinsfile or job configuration
triggers {
    cron('H/15 * * * *')  // Every 15 minutes
}
```

## 🎯 Success Criteria

### ✅ Build Success Indicators
- **All stages complete**: 7/7 stages passed
- **Tests passing**: 23/23 tests passed
- **Reports generated**: HTML, JSON, coverage reports
- **Artifacts archived**: All reports available for download

### 📈 Performance Metrics
- **Build time**: < 5 minutes
- **Test execution**: < 2 minutes
- **Success rate**: 100% (all tests pass)
- **Coverage**: > 90% code coverage

---

## 🚀 Quick Start Commands

### Local Testing (Before Jenkins)
```bash
# Test the framework locally first
python -m pytest tests/test_books_api.py -v

# Generate reports
python -m pytest --html=reports/report.html --self-contained-html --cov=tests --cov-report=html:reports/coverage
```

### Jenkins Verification
```bash
# Check Jenkins status
sudo systemctl status jenkins

# View Jenkins logs
sudo tail -f /var/log/jenkins/jenkins.log

# Access Jenkins
open http://localhost:8080
```

---

**🎉 Your API Automation Framework is now ready for Jenkins CI/CD!**

The framework includes:
- ✅ Complete test suite (23 tests)
- ✅ Robust error handling
- ✅ Multiple report formats
- ✅ CI/CD pipeline configuration
- ✅ Comprehensive documentation
