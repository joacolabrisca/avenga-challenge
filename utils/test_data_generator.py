## Test data generator module for creating realistic test data for the Books API.

import json
import random
import logging
from typing import Dict, Any, List
from datetime import datetime
from faker import Faker

from config.config import Config


## Generate realistic test data for Books API testing
class TestDataGenerator:
    
    ## Initialize the test data generator
    def __init__(self, locale: str = 'en_US'):
        self.fake = Faker(locale)
        self.fake.seed_instance(random.randint(1, 1000))
        logging.info(f"Test data generator initialized with locale: {locale}")


    ## Generate valid book data
    def generate_book_data(self, book_id: int = None) -> Dict[str, Any]:
        if book_id is None:
            book_id = random.randint(1000, 9999)
        
        # Generate realistic book data
        book_data = {
            "id": book_id,
            "title": self.fake.catch_phrase(),
            "description": self.fake.text(max_nb_chars=200),
            "pageCount": random.randint(50, 1000),
            "excerpt": self.fake.text(max_nb_chars=500),
            "publishDate": self.fake.date_between(
                start_date='-10y', 
                end_date='today'
            ).strftime('%Y-%m-%d')
        }
        
        logging.debug(f"Generated book data with ID: {book_id}")
        return book_data


    ## Generate invalid book data for negative testing
    def generate_invalid_book_data(self, invalid_field: str = None) -> Dict[str, Any]:
        # Start with valid data
        valid_data = self.generate_book_data()
        
        if invalid_field == "missing_required":
            # Remove required fields
            valid_data.pop("title", None)
            valid_data.pop("description", None)
            valid_data.pop("pageCount", None)
        elif invalid_field == "wrong_types":
            # Use wrong data types
            valid_data["id"] = "not_an_integer"
            valid_data["pageCount"] = "not_a_number"
            valid_data["title"] = 12345
        elif invalid_field == "empty_values":
            # Use empty values
            valid_data["title"] = ""
            valid_data["description"] = ""
            valid_data["excerpt"] = ""
        elif invalid_field == "negative_values":
            # Use negative values
            valid_data["id"] = -1
            valid_data["pageCount"] = -100
        elif invalid_field == "invalid_date":
            # Use invalid date format
            valid_data["publishDate"] = "invalid-date-format"
        else:
            # Default: mix of invalid data
            valid_data["title"] = ""  # Empty title
            valid_data["pageCount"] = -50  # Negative page count
            valid_data["publishDate"] = "not-a-date"  # Invalid date
        
        logging.debug(f"Generated invalid book data with field: {invalid_field}")
        return valid_data


    ## Generate edge case data for boundary testing
    def generate_edge_case_data(self) -> List[Dict[str, Any]]:
        edge_cases = []
        
        # Very long strings
        long_title = "A" * 1000
        long_description = "B" * 2000
        long_excerpt = "C" * 5000
        
        edge_cases.append({
            "name": "very_long_strings",
            "data": {
                "id": random.randint(1000, 9999),
                "title": long_title,
                "description": long_description,
                "pageCount": 500,
                "excerpt": long_excerpt,
                "publishDate": datetime.now().strftime('%Y-%m-%d')
            }
        })
        
        # Special characters
        special_chars = "ñáéíóú@#$%^&*()_+-=[]{}|;':\",./<>?"
        edge_cases.append({
            "name": "special_characters",
            "data": {
                "id": random.randint(1000, 9999),
                "title": f"Book with {special_chars}",
                "description": f"Description with {special_chars}",
                "pageCount": 300,
                "excerpt": f"Excerpt with {special_chars}",
                "publishDate": datetime.now().strftime('%Y-%m-%d')
            }
        })
        
        # Extreme values
        edge_cases.append({
            "name": "extreme_values",
            "data": {
                "id": 999999999,
                "title": "Book with extreme values",
                "description": "Description",
                "pageCount": 999999,
                "excerpt": "Excerpt",
                "publishDate": "1900-01-01T00:00:00.000Z"
            }
        })
        
        # Unicode characters
        unicode_text = "Unicode: 你好世界 🌍 🚀 📚"
        edge_cases.append({
            "name": "unicode_characters",
            "data": {
                "id": random.randint(1000, 9999),
                "title": unicode_text,
                "description": f"Description with {unicode_text}",
                "pageCount": 400,
                "excerpt": f"Excerpt with {unicode_text}",
                "publishDate": datetime.now().strftime('%Y-%m-%d')
            }
        })
        
        # SQL injection attempt
        sql_injection = "'; DROP TABLE books; --"
        edge_cases.append({
            "name": "sql_injection",
            "data": {
                "id": random.randint(1000, 9999),
                "title": sql_injection,
                "description": f"Description with {sql_injection}",
                "pageCount": 250,
                "excerpt": f"Excerpt with {sql_injection}",
                "publishDate": datetime.now().strftime('%Y-%m-%d')
            }
        })
        
        # XSS attempt
        xss_attempt = "<script>alert('XSS')</script>"
        edge_cases.append({
            "name": "xss_attempt",
            "data": {
                "id": random.randint(1000, 9999),
                "title": xss_attempt,
                "description": f"Description with {xss_attempt}",
                "pageCount": 350,
                "excerpt": f"Excerpt with {xss_attempt}",
                "publishDate": datetime.now().strftime('%Y-%m-%d')
            }
        })
        
        logging.debug(f"Generated {len(edge_cases)} edge case data sets")
        return edge_cases


    ## Generate multiple books for bulk testing
    def generate_multiple_books(self, count: int) -> List[Dict[str, Any]]:
        books = []
        for i in range(count):
            book_data = self.generate_book_data()
            books.append(book_data)
        
        logging.debug(f"Generated {count} books for bulk testing")
        return books


    ## Save generated test data to a JSON file
    def save_test_data_to_file(self, filename: str = 'test_books.json'):
        test_data = {
            "valid_books": self.generate_multiple_books(5),
            "invalid_books": [
                self.generate_invalid_book_data("missing_required"),
                self.generate_invalid_book_data("wrong_types"),
                self.generate_invalid_book_data("empty_values")
            ],
            "edge_cases": self.generate_edge_case_data()
        }
        
        filepath = Config.TEST_DATA_DIR / filename
        filepath.parent.mkdir(exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2, ensure_ascii=False)
        
        logging.info(f"Test data saved to {filepath}")


    ## Load test data from a JSON file, or generate if file doesn't exist
    def load_test_data_from_file(self, filename: str = 'test_books.json') -> Dict[str, Any]:
        filepath = Config.TEST_DATA_DIR / filename
        
        try:
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    test_data = json.load(f)
                logging.info(f"Test data loaded from {filepath}")
                return test_data
            else:
                logging.info(f"Test data file {filepath} not found, generating new data")
                self.save_test_data_to_file(filename)
                # Load the newly created file
                with open(filepath, 'r', encoding='utf-8') as f:
                    test_data = json.load(f)
                return test_data
        except Exception as e:
            logging.error(f"Error loading test data from {filepath}: {e}")
            logging.info("Generating fallback test data")
            return self._generate_fallback_data()


    ## Generate fallback test data when file loading fails
    def _generate_fallback_data(self) -> Dict[str, Any]:
        return {
            "valid_books": self.generate_multiple_books(3),
            "invalid_books": [
                self.generate_invalid_book_data("missing_required"),
                self.generate_invalid_book_data("wrong_types")
            ],
            "edge_cases": self.generate_edge_case_data()[:2]  # Only first 2 edge cases
        } 
