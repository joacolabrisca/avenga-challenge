## Configuration module for the API automation framework.

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


## Centralized configuration for the API automation framework
class Config:
    
    # API Configuration
    API_BASE_URL: str = os.getenv('API_BASE_URL', 'https://fakerestapi.azurewebsites.net')
    API_TIMEOUT: int = int(os.getenv('TIMEOUT', '30'))
    API_VERSION: str = 'v1'
    
    # Test Configuration
    TEST_TIMEOUT: int = int(os.getenv('TEST_TIMEOUT', '60'))
    MAX_RETRIES: int = int(os.getenv('MAX_RETRIES', '3'))
    RETRY_DELAY: int = int(os.getenv('RETRY_DELAY', '1'))
    
    # Reporting Configuration
    REPORTS_DIR: Path = Path('reports')
    HTML_REPORT_FILE: str = 'report.html'
    JSON_REPORT_FILE: str = 'report.json'
    JUNIT_REPORT_FILE: str = 'junit.xml'
    COVERAGE_REPORT_DIR: str = 'coverage'
    
    # Test Data Configuration
    TEST_DATA_DIR: Path = Path('tests/test_data')
    TEST_DATA_FILE: str = 'test_books.json'
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Performance Configuration
    PERFORMANCE_TIMEOUT: int = int(os.getenv('PERFORMANCE_TIMEOUT', '10'))
    MAX_RESPONSE_SIZE: int = int(os.getenv('MAX_RESPONSE_SIZE', '1048576'))  # 1MB
    
    # Security Configuration
    ALLOW_INSECURE_REQUESTS: bool = os.getenv('ALLOW_INSECURE_REQUESTS', 'false').lower() == 'true'
    
    
        
    ## Get the books endpoint URL
    @classmethod
    def get_books_endpoint(cls) -> str:
        return f"{cls.API_BASE_URL}/api/{cls.API_VERSION}/Books"
    
    
    ## Get the book by ID endpoint URL
    @classmethod
    def get_book_by_id_endpoint(cls, book_id: int) -> str:
        return f"{cls.get_books_endpoint()}/{book_id}"
    
    
        
    ## Validate the configuration settings
    @classmethod
    def validate_config(cls) -> bool:
        try:
            # Validate API URL
            if not cls.API_BASE_URL.startswith(('http://', 'https://')):
                print(f"Invalid API_BASE_URL: {cls.API_BASE_URL}")
                return False
            
            # Validate timeouts
            if cls.API_TIMEOUT <= 0 or cls.TEST_TIMEOUT <= 0:
                print("Timeouts must be positive values")
                return False
            
            # Validate retry settings
            if cls.MAX_RETRIES < 0 or cls.RETRY_DELAY < 0:
                print("Retry settings must be non-negative")
                return False
            
            # Validate log level
            valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
            if cls.LOG_LEVEL not in valid_log_levels:
                print(f"Invalid LOG_LEVEL: {cls.LOG_LEVEL}")
                return False
            
            return True
            
        except Exception as e:
            print(f"Configuration validation error: {e}")
            return False
    
    

# Create a global config instance
config = Config()


# Validate configuration on import
if not config.validate_config():
    print("Warning: Configuration validation failed. Please check your settings.") 
