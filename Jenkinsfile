pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.11'
        VENV_NAME = 'venv'
        REPORTS_DIR = 'reports'
        PYTHONPATH = "${WORKSPACE}"
    }
    
    options {
        timeout(time: 10, unit: 'MINUTES')
        timestamps()
        disableConcurrentBuilds()
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "🔍 Checking out code from repository..."
                    checkout scm
                    echo "✅ Checkout completed successfully"
                }
            }
        }
        
        stage('Setup Environment') {
            steps {
                script {
                    echo "🔧 Setting up Python environment..."
                    
                    // Create reports directory
                    if (isUnix()) {
                        sh '''
                            mkdir -p reports
                            echo "Reports directory created"
                        '''
                    } else {
                        bat '''
                            if not exist reports mkdir reports
                            echo Reports directory created
                        '''
                    }
                    
                    // Check Python installation
                    if (isUnix()) {
                        sh '''
                            python --version || python3 --version
                            echo "Python version check completed"
                        '''
                    } else {
                        bat '''
                            python --version
                            echo Python version check completed
                        '''
                    }
                    
                    echo "✅ Environment setup completed"
                }
            }
        }
        
        stage('Install Dependencies') {
            steps {
                script {
                    echo "📦 Installing Python dependencies..."
                    
                    // Create virtual environment
                    if (isUnix()) {
                        sh '''
                            python -m venv venv || python3 -m venv venv
                            echo "Virtual environment created"
                        '''
                    } else {
                        bat '''
                            python -m venv venv
                            echo Virtual environment created
                        '''
                    }
                    
                    // Activate virtual environment and install dependencies
                    if (isUnix()) {
                        sh '''
                            if [ "$(uname)" == "Darwin" ]; then
                                # macOS
                                source venv/bin/activate
                            elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
                                # Linux
                                source venv/bin/activate
                            fi
                            
                            pip install --upgrade pip
                            pip install -r requirements.txt
                            echo "Dependencies installed successfully"
                        '''
                    } else {
                        bat '''
                            venv\\Scripts\\python.exe -m pip install --upgrade pip
                            venv\\Scripts\\python.exe -m pip install -r requirements.txt
                            echo Dependencies installed successfully
                        '''
                    }
                    
                    echo "✅ Dependencies installation completed"
                }
            }
        }
        

        
        stage('Run Tests') {
            steps {
                script {
                    echo "🧪 Running API automation tests..."
                    
                    if (isUnix()) {
                        // Run tests with detailed output
                        sh '''
                            if [ "$(uname)" == "Darwin" ]; then
                                source venv/bin/activate
                            elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
                                source venv/bin/activate
                            fi
                            
                            # Run tests with detailed output
                            python -m pytest tests/test_books_api.py -v --tb=short
                            echo "Test execution completed"
                        '''
                    } else {
                        // Run tests with detailed output
                        bat '''
                            venv\\Scripts\\python.exe -m pytest tests/test_books_api.py -v --tb=short
                            echo Test execution completed
                        '''
                    }
                    
                    echo "✅ Test execution completed"
                }
            }
        }
        
        stage('Generate Reports') {
            steps {
                script {
                    echo "📊 Generating test reports..."
                    
                    if (isUnix()) {
                        // Generate reports with detailed output
                        sh '''
                            if [ "$(uname)" == "Darwin" ]; then
                                source venv/bin/activate
                            elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
                                source venv/bin/activate
                            fi
                            
                            # Generate HTML report
                            python -m pytest tests/test_books_api.py --html=reports/report.html --self-contained-html --tb=short
                            
                            # Generate coverage report
                            python -m pytest tests/test_books_api.py --cov=tests --cov-report=html:reports/coverage --cov-report=term-missing
                            
                            # Generate JSON report
                            python -m pytest tests/test_books_api.py --json-report --json-report-file=reports/report.json
                            
                            echo "Reports generated successfully"
                        '''
                    } else {
                        // Generate reports with detailed output
                        bat '''
                            venv\\Scripts\\python.exe -m pytest tests/test_books_api.py --html=reports/report.html --self-contained-html --tb=short
                            venv\\Scripts\\python.exe -m pytest tests/test_books_api.py --cov=tests --cov-report=html:reports/coverage --cov-report=term-missing
                            venv\\Scripts\\python.exe -m pytest tests/test_books_api.py --json-report --json-report-file=reports/report.json
                            echo Reports generated successfully
                        '''
                    }
                    
                    echo "✅ Report generation completed"
                }
            }
        }
        
        stage('Archive Reports') {
            steps {
                script {
                    echo "📁 Archiving test reports..."
                    
                    // Archive HTML report
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports',
                        reportFiles: 'report.html',
                        reportName: 'HTML Test Report',
                        reportTitles: 'API Automation Test Results'
                    ])
                    
                    // Archive coverage report
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports/coverage',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report',
                        reportTitles: 'Code Coverage Analysis'
                    ])
                    
                    // Archive JSON report
                    archiveArtifacts(
                        artifacts: 'reports/report.json',
                        fingerprint: true,
                        allowEmptyArchive: false
                    )
                    
                    echo "✅ Report archiving completed"
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo "🧹 Cleaning up workspace..."
                
                // Clean up virtual environment
                if (isUnix()) {
                    sh '''
                        rm -rf venv || echo "Virtual environment cleanup completed"
                    '''
                } else {
                    bat '''
                        rmdir /s /q venv 2>nul || echo Virtual environment cleanup completed
                    '''
                }
                
                echo "✅ Cleanup completed"
            }
        }
        
        success {
            script {
                // Display test results
                echo "🎉 Build completed successfully!"
                echo "📊 Test Results:"
                echo "   - HTML Report: Available in build artifacts"
                echo "   - Coverage Report: Available in build artifacts"
                echo "   - JSON Report: Available in build artifacts"
            }
        }
        
        failure {
            script {
                // Display failure message
                echo "❌ Build failed!"
                echo "🔍 Check the console output for details"
                echo "📧 Consider checking:"
                echo "   - Python installation"
                echo "   - Network connectivity"
                echo "   - API availability"
            }
        }
        
        unstable {
            script {
                // Display unstable message
                echo "⚠️ Build unstable - some tests may have failed"
                echo "📊 Check test reports for details"
            }
        }
    }
} 
