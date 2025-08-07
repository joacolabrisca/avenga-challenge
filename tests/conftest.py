## PyTest configuration and fixtures for Books API testing.

import pytest
import logging
from typing import Dict, Any, List, Generator
from pathlib import Path

from utils.api_client import BooksAPIClient
from utils.test_data_generator import TestDataGenerator
from utils.validators import APIResponseValidator, ResponseAsserter
from config.config import Config


## Provide a Books API client for the entire test session
@pytest.fixture(scope="session")
def api_client() -> BooksAPIClient:
    return BooksAPIClient()


## Load test data from JSON file or generate if not found
@pytest.fixture(scope="session")
def test_data() -> Dict[str, Any]:
    generator = TestDataGenerator()
    return generator.load_test_data_from_file()


## Generate valid book data for individual tests
@pytest.fixture(scope="function")
def valid_book_data() -> Dict[str, Any]:
    generator = TestDataGenerator()
    return generator.generate_book_data()


## Generate multiple valid book data sets for testing
@pytest.fixture(scope="function")
def multiple_books_data() -> List[Dict[str, Any]]:
    generator = TestDataGenerator()
    return [generator.generate_book_data() for _ in range(3)]


## Generate invalid book data for negative testing
@pytest.fixture(scope="function")
def invalid_book_data() -> Dict[str, Any]:
    generator = TestDataGenerator()
    return generator.generate_invalid_book_data()


## Get an existing book ID for testing, or create one if none exists
@pytest.fixture(scope="session")
def existing_book_id(api_client: BooksAPIClient) -> int:
    try:
        response = api_client.get_all_books()
        if response.status_code == 200:
            books = response.json()
            if books:
                return books[0]['id']
    except Exception as e:
        logging.warning(f"Could not retrieve existing books: {e}")
    
    # If no existing books found, create one
    generator = TestDataGenerator()
    book_data = generator.generate_book_data()
    try:
        response = api_client.create_book(book_data)
        if response.status_code == 200:
            created_book = response.json()
            logging.info(f"Created test book with ID {created_book['id']}")
            return created_book['id']
    except Exception as e:
        logging.error(f"Could not create test book: {e}")
    
    # Fallback to a known ID
    return 1


## Create a book before test and delete it after test completion
@pytest.fixture(scope="function")
def created_book(api_client: BooksAPIClient, valid_book_data: Dict[str, Any]) -> Generator[Dict[str, Any], None, None]:
    response = api_client.create_book(valid_book_data)
    assert response.status_code == 200, f"Error creating book: {response.text}"
    created_book = response.json()
    
    yield created_book
    
    try:
        api_client.delete_book(created_book['id'])
    except Exception as e:
        logging.warning(f"Could not delete book {created_book['id']}: {e}")


## Generate updated book data for testing updates
@pytest.fixture(scope="function")
def updated_book_data(valid_book_data: Dict[str, Any]) -> Dict[str, Any]:
    updated_data = valid_book_data.copy()
    updated_data['title'] = f"Updated {updated_data['title']}"
    updated_data['description'] = f"Updated {updated_data['description']}"
    return updated_data


## Generate edge case data for testing boundary conditions
@pytest.fixture(scope="function")
def edge_cases_data() -> Dict[str, Any]:
    generator = TestDataGenerator()
    return generator.generate_edge_case_data()


## Provide API response validator for the entire test session
@pytest.fixture(scope="session")
def validator() -> APIResponseValidator:
    return APIResponseValidator()


## Provide response asserter for the entire test session
@pytest.fixture(scope="session")
def asserter() -> ResponseAsserter:
    return ResponseAsserter()


 
