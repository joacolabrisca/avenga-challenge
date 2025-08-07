# API Automation Framework - Books API Testing

A comprehensive API automation framework built with PyTest and Jenkins for testing the FakeRestAPI Books API. This project demonstrates industry best practices for API testing automation with complete test coverage, robust error handling, and CI/CD integration.

## 🎯 Project Overview

This framework provides automated testing for the Books API with the following features:

- **Complete CRUD Operations Testing**: Full coverage of GET, POST, PUT, DELETE endpoints
- **Comprehensive Test Coverage**: 23 tests covering happy paths, negative cases, edge cases, and integration scenarios
- **Robust Data Validation**: JSON Schema and Pydantic validation for response verification
- **Dynamic Test Data Generation**: Using Faker for realistic test data
- **CI/CD Integration**: Jenkins pipeline for automated testing
- **Multiple Report Formats**: HTML, JSON, and coverage reports
- **Clean Architecture**: Modular design following SOLID principles
- **Optimized Pipeline**: Streamlined Jenkins pipeline without unnecessary steps

## 📋 Test Coverage Summary

### ✅ Endpoints Covered
- **GET /api/v1/Books** - Retrieve all books
- **GET /api/v1/Books/{id}** - Retrieve specific book by ID
- **POST /api/v1/Books** - Create new book
- **PUT /api/v1/Books/{id}** - Update existing book
- **DELETE /api/v1/Books/{id}** - Delete book

### ✅ Test Categories (23 Total Tests)
- **Happy Path Tests (5)**: Basic functionality verification
- **Negative Tests (7)**: Error handling and edge cases
- **Edge Case Tests (4)**: Boundary conditions and special scenarios
- **Integration Tests (1)**: Complete CRUD lifecycle
- **Regression Tests (2)**: Response consistency verification
- **Performance Tests (1)**: Response time validation
- **Data Validation Tests (2)**: Schema and data structure validation

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/joacolabrisca/avenga_challenge_solution.git
   cd avenga_challenge_solution
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment (optional)**
   ```bash
   cp env.example .env
   # Edit .env file with your configuration
   ```

### Running Tests

#### Basic Test Execution
```bash
# Run all tests
python -m pytest

# Run with verbose output
python -m pytest -v

# Run specific test file
python -m pytest tests/test_books_api.py
```

#### Using the Test Runner Script
```bash
# Run all tests with default settings
python run_tests.py

# Generate HTML report
python run_tests.py --html

# Run with coverage
python run_tests.py --coverage
```

#### Advanced Test Execution
```bash
# Generate multiple report formats
python -m pytest --html=reports/report.html --self-contained-html --cov=tests --cov-report=html:reports/coverage

# Run specific test method
python -m pytest tests/test_books_api.py::TestBooksAPI::test_get_all_books
```

## 📊 Reporting

### Available Reports
- **HTML Reports**: Self-contained HTML with detailed test results
- **JSON Reports**: Machine-readable test results
- **Coverage Reports**: Code coverage analysis

### Report Locations
- HTML Report: `reports/report.html`
- Coverage Report: `reports/coverage/index.html`
- JSON Report: `reports/report.json`

## 🔄 CI/CD Integration

### Jenkins Pipeline
The `Jenkinsfile` provides a streamlined CI/CD pipeline:

```groovy
pipeline {
    agent any
    
    stages {
        stage('Checkout') { ... }
        stage('Setup Environment') { ... }
        stage('Install Dependencies') { ... }
        stage('Run Tests') { ... }
        stage('Generate Reports') { ... }
        stage('Archive Reports') { ... }
    }
}
```

### Pipeline Features
- **Multi-platform Support**: Windows and Unix environments
- **Dependency Management**: Automatic package installation
- **Test Execution**: Comprehensive test suite execution
- **Report Archiving**: Automatic report collection
- **Optimized Performance**: Removed unnecessary code quality checks for faster execution

## 🛠️ Jenkins Installation & Configuration Guide

### Prerequisites
- **Java 11 or higher** (Java 17 recommended)
- **Git** installed and configured
- **GitHub account** with repository access

### Step 1: Install Java

#### Windows
```powershell
# Download and install Java 17 from Oracle or OpenJDK
# Set JAVA_HOME environment variable
setx JAVA_HOME "C:\Program Files\Java\jdk-17"
setx PATH "%PATH%;%JAVA_HOME%\bin"
```

#### Linux/Mac
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install openjdk-17-jdk

# macOS
brew install openjdk@17
```

### Step 2: Install Jenkins

#### Download Jenkins WAR
```bash
# Create Jenkins directory
mkdir jenkins
cd jenkins

# Download Jenkins WAR file
curl -L https://get.jenkins.io/war-stable/latest/jenkins.war -o jenkins.war
```

#### Start Jenkins
```bash
# Start Jenkins on port 8081 (to avoid conflicts)
java -jar jenkins.war --httpPort=8081
```

#### Access Jenkins
1. Open browser: `http://localhost:8081`
2. Get initial admin password:
   ```bash
   # Windows
   type %USERPROFILE%\.jenkins\secrets\initialAdminPassword
   
   # Linux/Mac
   cat ~/.jenkins/secrets/initialAdminPassword
   ```

### Step 3: Jenkins Initial Setup

1. **Install Suggested Plugins**
   - Git plugin
   - Pipeline plugin
   - HTML Publisher plugin
   - Coverage plugin

2. **Create Admin User**
   - Username: `admin`
   - Password: `your-secure-password`

3. **Configure Jenkins URL**
   - URL: `http://localhost:8081`

### Step 4: Configure GitHub Integration

#### Create GitHub Personal Access Token
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes:
   - `repo` (full control of private repositories)
   - `admin:repo_hook` (manage repository hooks)
4. Copy the token (you'll need it for Jenkins)

#### Configure Jenkins Credentials
1. Go to Jenkins → Manage Jenkins → Credentials
2. Click "System" → "Global credentials" → "Add Credentials"
3. Configure:
   - **Kind**: Username with password
   - **Scope**: Global
   - **Username**: Your GitHub username
   - **Password**: Your GitHub Personal Access Token
   - **ID**: `github-token`
   - **Description**: GitHub Personal Access Token

### Step 5: Create Jenkins Pipeline Job

#### Create New Job
1. Go to Jenkins → New Item
2. Enter job name: `API-Automation-Framework`
3. Select "Pipeline"
4. Click "OK"

#### Configure Pipeline
1. **General Settings**:
   - ✅ Discard old builds
   - ✅ GitHub project: `https://github.com/joacolabrisca/avenga_challenge_solution`

2. **Build Triggers**:
   - ✅ Poll SCM: `H/2 * * * *` (check every 2 minutes)
   - OR for webhooks (see webhook configuration below)

3. **Pipeline Definition**:
   - **Definition**: Pipeline script from SCM
   - **SCM**: Git
   - **Repository URL**: `https://github.com/joacolabrisca/avenga_challenge_solution.git`
   - **Credentials**: Select your GitHub token
   - **Branch Specifier**: `*/master`
   - **Script Path**: `Jenkinsfile`

4. **Save the configuration**

### Step 6: Webhook Configuration (Optional)

#### For Local Development (ngrok)
If you want to use webhooks with localhost:

1. **Install ngrok**
   ```bash
   # Download ngrok from https://ngrok.com/
   # Extract and add to PATH
   ```

2. **Expose Jenkins to internet**
   ```bash
   ngrok http 8081
   # Note the HTTPS URL provided (e.g., https://abc123.ngrok.io)
   ```

3. **Configure GitHub Webhook**
   - Go to your GitHub repository → Settings → Webhooks
   - Click "Add webhook"
   - **Payload URL**: `https://abc123.ngrok.io/github-webhook/`
   - **Content type**: `application/json`
   - **Events**: Select "Just the push event"
   - Click "Add webhook"

4. **Update Jenkins Job**
   - Go to your Jenkins job → Configure
   - **Build Triggers**: ✅ GitHub hook trigger for GITScm polling
   - Save

#### For Production Server
If Jenkins is on a public server:

1. **Configure GitHub Webhook**
   - Go to your GitHub repository → Settings → Webhooks
   - Click "Add webhook"
   - **Payload URL**: `http://your-jenkins-server:8081/github-webhook/`
   - **Content type**: `application/json`
   - **Events**: Select "Just the push event"
   - Click "Add webhook"

2. **Update Jenkins Job**
   - Go to your Jenkins job → Configure
   - **Build Triggers**: ✅ GitHub hook trigger for GITScm polling
   - Save

### Step 7: Test the Pipeline

#### Manual Trigger
1. Go to your Jenkins job
2. Click "Build Now"
3. Monitor the build progress
4. Check build artifacts and reports

#### Automatic Trigger (Webhook)
1. Make a change to your repository
2. Push to GitHub
3. Jenkins should automatically trigger a build
4. Monitor the build progress

## 🎯 Test Categories

### Happy Path Tests
Basic functionality verification for critical paths:
- GET all books
- GET book by ID
- POST create book
- PUT update book
- DELETE book

### Negative Tests
Error handling and edge case validation:
- Invalid book IDs
- Missing required fields
- Wrong data types
- Non-existent resources
- Boundary conditions

### Edge Case Tests
Boundary conditions and special scenarios:
- Very long strings
- Special characters
- Unicode content
- SQL injection attempts
- XSS prevention

### Integration Tests
End-to-end workflow validation:
- Complete CRUD lifecycle
- Data consistency verification
- State management testing

### Performance Tests
Response time and performance validation:
- Response time limits
- Throughput testing
- Resource utilization

## 🛠️ Development

### Adding New Tests
1. Create test method in `tests/test_books_api.py`
2. Follow naming convention: `test_<description>`
3. Add proper assertions and error handling

### Extending the Framework
1. **New API Endpoints**: Add methods to `BooksAPIClient`
2. **Custom Validators**: Extend `APIResponseValidator`
3. **Test Data**: Add scenarios to `TestDataGenerator`
4. **Configuration**: Update `Config` class

### Code Quality
- **Type Hints**: All functions include type annotations
- **Comments**: All functions have descriptive comments
- **Error Handling**: Robust exception management
- **Logging**: Detailed logging for debugging

## 📈 Performance Metrics

### Test Execution
- **Total Tests**: 23
- **Execution Time**: ~12 seconds
- **Success Rate**: 100% (all tests pass)
- **Coverage**: Comprehensive endpoint coverage

### API Performance
- **Response Time**: < 5 seconds (configurable)
- **Retry Logic**: 3 attempts with exponential backoff
- **Timeout**: 30 seconds per request
- **Concurrent Support**: Parallel test execution

## 📁 Project Structure

```
├── config/
│   ├── __init__.py
│   └── config.py              # Configuration management
├── utils/
│   ├── __init__.py
│   ├── api_client.py          # HTTP client and API interactions
│   ├── test_data_generator.py # Test data generation
│   └── validators.py          # Response validation
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # PyTest fixtures
│   ├── test_books_api.py      # Main test suite
│   └── test_data/
│       ├── __init__.py
│       └── test_books.json    # Static test data
├── reports/                   # Generated test reports
├── Jenkinsfile               # CI/CD pipeline definition
├── requirements.txt          # Python dependencies
├── pytest.ini               # PyTest configuration
├── run_tests.py             # Test execution utility
├── env.example              # Environment variables template
├── jenkins-setup.md         # Jenkins setup guide
└── README.md                # This file
```
