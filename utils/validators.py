## Validation module for API responses and data structures.

import json
import logging
from typing import Dict, Any, List
from datetime import datetime
from jsonschema import validate, ValidationError
from pydantic import BaseModel, field_validator


## Pydantic model for book data validation
class BookSchema(BaseModel):
    
    id: int
    title: str
    description: str
    pageCount: int
    excerpt: str
    publishDate: str
    
    ## Validate book ID is positive
    @field_validator('id')
    @classmethod
    def validate_id(cls, v):
        if v <= 0:
            raise ValueError('Book ID must be positive')
        return v
    
    ## Validate title is not empty
    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()
    
    ## Validate description is not empty
    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        if not v or not v.strip():
            raise ValueError('Description cannot be empty')
        return v.strip()
    
    ## Validate page count is positive
    @field_validator('pageCount')
    @classmethod
    def validate_page_count(cls, v):
        if v <= 0:
            raise ValueError('Page count must be positive')
        return v
    
    ## Validate excerpt is a string
    @field_validator('excerpt')
    @classmethod
    def validate_excerpt(cls, v):
        if not isinstance(v, str):
            raise ValueError('Excerpt must be a string')
        return v
    
    ## Validate publish date format
    @field_validator('publishDate')
    @classmethod
    def validate_publish_date(cls, v):
        try:
            datetime.fromisoformat(v.replace('Z', '+00:00'))
            return v
        except ValueError:
            raise ValueError('Invalid date format. Expected ISO format')


## Validator for API responses using JSON schemas
class APIResponseValidator:
    
    # JSON Schema for a single book
    BOOK_SCHEMA = {
        "type": "object",
        "properties": {
            "id": {"type": "integer", "minimum": 1},
            "title": {"type": "string", "minLength": 1},
            "description": {"type": "string", "minLength": 1},
            "pageCount": {"type": "integer", "minimum": 1},
            "excerpt": {"type": "string"},
            "publishDate": {"type": "string", "format": "date-time"}
        },
        "required": ["id", "title", "description", "pageCount", "excerpt", "publishDate"],
        "additionalProperties": False
    }
    
    # JSON Schema for a list of books
    BOOKS_LIST_SCHEMA = {
        "type": "array",
        "items": BOOK_SCHEMA,
        "minItems": 0
    }
    
    ## Validate a single book response against the schema
    @classmethod
    def validate_book_response(cls, response_data: Dict[str, Any]) -> bool:
        try:
            validate(instance=response_data, schema=cls.BOOK_SCHEMA)
            logging.debug("Book response validation passed")
            return True
        except ValidationError as e:
            logging.warning(f"Book response validation failed: {e}")
            return False
    
    ## Validate a list of books response against the schema
    @classmethod
    def validate_books_list_response(cls, response_data: List[Dict[str, Any]]) -> bool:
        try:
            validate(instance=response_data, schema=cls.BOOKS_LIST_SCHEMA)
            logging.debug("Books list response validation passed")
            return True
        except ValidationError as e:
            logging.warning(f"Books list response validation failed: {e}")
            return False
    
    ## Validate book data using Pydantic model
    @classmethod
    def validate_book_data(cls, book_data: Dict[str, Any]) -> List[str]:
        try:
            BookSchema(**book_data)
            logging.debug("Book data validation passed")
            return []
        except Exception as e:
            logging.warning(f"Book data validation failed: {e}")
            return [str(e)]


## Static methods for common response assertions
class ResponseAsserter:
    
    ## Assert that response has the expected status code
    @staticmethod
    def assert_status_code(response, expected_status: int):
        assert response.status_code == expected_status, \
            f"Expected status code {expected_status}, got {response.status_code}"
    
    ## Assert that response has the expected content type
    @staticmethod
    def assert_content_type(response, expected_type: str = "application/json"):
        content_type = response.headers.get('content-type', '')
        assert expected_type in content_type, \
            f"Expected content type containing '{expected_type}', got '{content_type}'"
    
    ## Assert that book data has the correct structure
    @staticmethod
    def assert_book_structure(book_data: Dict[str, Any]):
        required_fields = ['id', 'title', 'description', 'pageCount', 'excerpt', 'publishDate']
        
        for field in required_fields:
            assert field in book_data, f"Missing required field: {field}"
        
        assert isinstance(book_data['id'], int), "ID must be an integer"
        assert isinstance(book_data['title'], str), "Title must be a string"
        assert isinstance(book_data['description'], str), "Description must be a string"
        assert isinstance(book_data['pageCount'], int), "PageCount must be an integer"
        assert isinstance(book_data['excerpt'], str), "Excerpt must be a string"
        assert isinstance(book_data['publishDate'], str), "PublishDate must be a string"
    
    ## Assert that books list data has the correct structure
    @staticmethod
    def assert_books_list_structure(books_data: List[Dict[str, Any]]):
        assert isinstance(books_data, list), "Books data must be a list"
        
        for book in books_data:
            ResponseAsserter.assert_book_structure(book)
    
    ## Assert that book content matches expected data
    @staticmethod
    def assert_book_content(book_data: Dict[str, Any], expected_data: Dict[str, Any]):
        # Check that all expected fields are present and match
        for field, expected_value in expected_data.items():
            if field in book_data:
                actual_value = book_data[field]
                
                # Special handling for publishDate to handle different formats
                if field == 'publishDate':
                    # Normalize both dates to YYYY-MM-DD format for comparison
                    expected_date = expected_value.split('T')[0] if 'T' in expected_value else expected_value
                    actual_date = actual_value.split('T')[0] if 'T' in actual_value else actual_value
                    assert actual_date == expected_date, \
                        f"Field '{field}' mismatch: expected '{expected_date}', got '{actual_date}'"
                else:
                    assert actual_value == expected_value, \
                        f"Field '{field}' mismatch: expected '{expected_value}', got '{actual_value}'"
    
    ## Assert that response is an error response
    @staticmethod
    def assert_error_response(response, expected_status: int = 400):
        ResponseAsserter.assert_status_code(response, expected_status)
        
        # Check if response contains error information
        try:
            error_data = response.json()
            assert 'error' in error_data or 'message' in error_data, \
                "Error response should contain 'error' or 'message' field"
        except json.JSONDecodeError:
            # Some APIs return plain text error messages
            assert response.text, "Error response should have content" 
