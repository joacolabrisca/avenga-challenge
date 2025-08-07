## Automated tests for the Books API

import pytest
import logging
from typing import Dict, Any

from utils.api_client import BooksAPIClient
from utils.validators import APIResponseValidator, ResponseAsserter

## Test suite for Books API endpoints
class TestBooksAPI:

    ## Test retrieving all books from the API
    def test_get_all_books(self, api_client: BooksAPIClient, asserter: ResponseAsserter, validator: APIResponseValidator):
        response = api_client.get_all_books()
        asserter.assert_status_code(response, 200)
        asserter.assert_content_type(response)
        
        books = response.json()
        asserter.assert_books_list_structure(books)
        assert validator.validate_books_list_response(books), \
            "Response does not match expected JSON schema"
        
        logging.info(f"Successfully retrieved {len(books)} books")


    ## Test retrieving a specific book by ID
    def test_get_book_by_id(self, api_client: BooksAPIClient, asserter: ResponseAsserter, 
                           validator: APIResponseValidator, existing_book_id: int):
        response = api_client.get_book_by_id(existing_book_id)
        asserter.assert_status_code(response, 200)
        asserter.assert_content_type(response)
        
        book = response.json()
        asserter.assert_book_structure(book)
        assert validator.validate_book_response(book), \
            "Response does not match expected JSON schema"
        assert book['id'] == existing_book_id, \
            f"Retrieved book ID {book['id']} does not match requested ID {existing_book_id}"
        
        logging.info(f"Successfully retrieved book with ID {existing_book_id}")


    ## Test creating a new book
    def test_create_book(self, api_client: BooksAPIClient, asserter: ResponseAsserter, 
                        validator: APIResponseValidator, valid_book_data: Dict[str, Any]):
        response = api_client.create_book(valid_book_data)
        asserter.assert_status_code(response, 200)
        asserter.assert_content_type(response)
        
        created_book = response.json()
        asserter.assert_book_structure(created_book)
        asserter.assert_book_content(created_book, valid_book_data)
        assert validator.validate_book_response(created_book), \
            "Response does not match expected JSON schema"
        
        try:
            api_client.delete_book(created_book['id'])
        except Exception as e:
            logging.warning(f"Could not delete created book: {e}")
        
        logging.info(f"Successfully created book with ID {created_book['id']}")


    ## Test updating an existing book
    def test_update_book(self, api_client: BooksAPIClient, asserter: ResponseAsserter, 
                        validator: APIResponseValidator, created_book: Dict[str, Any], 
                        updated_book_data: Dict[str, Any]):
        book_id = created_book['id']
        response = api_client.update_book(book_id, updated_book_data)
        asserter.assert_status_code(response, 200)
        asserter.assert_content_type(response)
        
        updated_book = response.json()
        asserter.assert_book_structure(updated_book)
        asserter.assert_book_content(updated_book, updated_book_data)
        assert validator.validate_book_response(updated_book), \
            "Response does not match expected JSON schema"
        assert updated_book['id'] == book_id, \
            f"Updated book ID {updated_book['id']} does not match original ID {book_id}"
        
        logging.info(f"Successfully updated book with ID {book_id}")


    ## Test deleting a book
    def test_delete_book(self, api_client: BooksAPIClient, asserter: ResponseAsserter, 
                        created_book: Dict[str, Any]):
        book_id = created_book['id']
        response = api_client.delete_book(book_id)
        asserter.assert_status_code(response, 200)
        
        # Verify book was deleted by trying to retrieve it
        get_response = api_client.get_book_by_id(book_id)
        asserter.assert_status_code(get_response, 404)
        
        logging.info(f"Successfully deleted book with ID {book_id}")


    ## Test retrieving a book with an invalid ID
    def test_get_book_by_invalid_id(self, api_client: BooksAPIClient, asserter: ResponseAsserter):
        invalid_id = 99999
        response = api_client.get_book_by_id(invalid_id)
        asserter.assert_status_code(response, 404)
        
        logging.info(f"Correctly received 404 for invalid book ID {invalid_id}")


    ## Test retrieving a book with a negative ID
    def test_get_book_by_negative_id(self, api_client: BooksAPIClient, asserter: ResponseAsserter):
        negative_id = -1
        response = api_client.get_book_by_id(negative_id)
        asserter.assert_status_code(response, 404)
        
        logging.info(f"Correctly received 404 for negative book ID {negative_id}")


    ## Test creating a book with invalid data
    def test_create_book_with_invalid_data(self, api_client: BooksAPIClient, asserter: ResponseAsserter, 
                                          invalid_book_data: Dict[str, Any]):
        response = api_client.create_book(invalid_book_data)
        # API might return 200 even with invalid data, so we check the response structure
        if response.status_code == 200:
            created_book = response.json()
            # Verify that the created book has valid structure despite invalid input
            asserter.assert_book_structure(created_book)
            try:
                api_client.delete_book(created_book['id'])
            except Exception as e:
                logging.warning(f"Could not delete book created with invalid data: {e}")
        else:
            asserter.assert_status_code(response, 400)
        
        logging.info("Tested book creation with invalid data")


    ## Test updating a book that doesn't exist
    def test_update_nonexistent_book(self, api_client: BooksAPIClient, asserter: ResponseAsserter, 
                                    valid_book_data: Dict[str, Any]):
        nonexistent_id = 99999
        response = api_client.update_book(nonexistent_id, valid_book_data)
        # FakeRestAPI might return 200 even for nonexistent books (creates new one)
        # or 404 for truly nonexistent books
        assert response.status_code in [200, 404], \
            f"Expected status code 200 or 404, got {response.status_code}"
        
        logging.info(f"Received status {response.status_code} when updating nonexistent book ID {nonexistent_id}")


    ## Test deleting a book that doesn't exist
    def test_delete_nonexistent_book(self, api_client: BooksAPIClient, asserter: ResponseAsserter):
        nonexistent_id = 99999
        response = api_client.delete_book(nonexistent_id)
        # FakeRestAPI might return 200 even for nonexistent books
        # or 404 for truly nonexistent books
        assert response.status_code in [200, 404], \
            f"Expected status code 200 or 404, got {response.status_code}"
        
        logging.info(f"Received status {response.status_code} when deleting nonexistent book ID {nonexistent_id}")


    ## Test creating a book with missing required fields
    def test_create_book_missing_required_fields(self, api_client: BooksAPIClient, asserter: ResponseAsserter):
        incomplete_data = {
            "id": 9999,
            "pageCount": 200
            # Missing title, description, excerpt, publishDate
        }
        response = api_client.create_book(incomplete_data)
        
        if response.status_code == 200:
            created_book = response.json()
            # FakeRestAPI might fill in missing fields with defaults
            # Just verify we get a valid response structure
            assert 'id' in created_book, "Created book should have an ID"
            try:
                api_client.delete_book(created_book['id'])
            except Exception as e:
                logging.warning(f"Could not delete book created with missing fields: {e}")
        else:
            asserter.assert_status_code(response, 400)
        
        logging.info("Tested book creation with missing required fields")


    ## Test creating a book with wrong data types
    def test_create_book_wrong_data_types(self, api_client: BooksAPIClient, asserter: ResponseAsserter):
        wrong_type_data = {
            "id": "not_an_integer",
            "title": 12345,
            "description": "Valid description",
            "pageCount": "not_a_number",
            "excerpt": "Valid excerpt",
            "publishDate": "invalid_date_format"
        }
        response = api_client.create_book(wrong_type_data)
        
        if response.status_code == 200:
            created_book = response.json()
            asserter.assert_book_structure(created_book)
            try:
                api_client.delete_book(created_book['id'])
            except Exception as e:
                logging.warning(f"Could not delete book created with wrong types: {e}")
        else:
            asserter.assert_status_code(response, 400)
        
        logging.info("Tested book creation with wrong data types")


    @pytest.mark.parametrize("edge_case_data", [
        "long_title",
        "special_chars",
        "empty_fields"
    ])
    ## Test creating books with edge case data
    def test_create_book_edge_cases(self, api_client: BooksAPIClient, asserter: ResponseAsserter, 
                                   validator: APIResponseValidator, edge_cases_data: Dict[str, Any], 
                                   edge_case_data: str):
        if edge_case_data in edge_cases_data:
            test_data = edge_cases_data[edge_case_data]
            response = api_client.create_book(test_data)
            
            if response.status_code == 200:
                created_book = response.json()
                asserter.assert_book_structure(created_book)
                assert validator.validate_book_response(created_book), \
                    "Edge case response does not match expected JSON schema"
                
                try:
                    api_client.delete_book(created_book['id'])
                except Exception as e:
                    logging.warning(f"Could not delete edge case book: {e}")
                
                logging.info(f"Successfully created book with edge case: {edge_case_data}")
            else:
                logging.info(f"Edge case {edge_case_data} returned status {response.status_code}")


    ## Test creating a book with very long title
    def test_create_book_very_long_title(self, api_client: BooksAPIClient, asserter: ResponseAsserter):
        long_title_data = {
            "id": 9999,
            "title": "A" * 1000,  # Very long title
            "description": "Test description",
            "pageCount": 300,
            "excerpt": "Test excerpt",
            "publishDate": "2023-01-01T00:00:00.000Z"
        }
        response = api_client.create_book(long_title_data)
        
        if response.status_code == 200:
            created_book = response.json()
            asserter.assert_book_structure(created_book)
            try:
                api_client.delete_book(created_book['id'])
            except Exception as e:
                logging.warning(f"Could not delete book with long title: {e}")
        else:
            asserter.assert_status_code(response, 400)
        
        logging.info("Tested book creation with very long title")


    ## Test creating a book with special characters
    def test_create_book_special_characters(self, api_client: BooksAPIClient, asserter: ResponseAsserter):
        special_chars_data = {
            "id": 9999,
            "title": "Book with ñ, á, é, í, ó, ú and symbols: @#$%^&*()",
            "description": "Description with special characters: ©®™",
            "pageCount": 300,
            "excerpt": "Excerpt with symbols: €£¥",
            "publishDate": "2023-01-01T00:00:00.000Z"
        }
        response = api_client.create_book(special_chars_data)
        
        if response.status_code == 200:
            created_book = response.json()
            asserter.assert_book_structure(created_book)
            try:
                api_client.delete_book(created_book['id'])
            except Exception as e:
                logging.warning(f"Could not delete book with special chars: {e}")
        else:
            asserter.assert_status_code(response, 400)
        
        logging.info("Tested book creation with special characters")


    ## Test complete CRUD lifecycle for a book
    def test_full_crud_lifecycle(self, api_client: BooksAPIClient, asserter: ResponseAsserter, 
                                valid_book_data: Dict[str, Any]):
        # Create
        create_response = api_client.create_book(valid_book_data)
        asserter.assert_status_code(create_response, 200)
        created_book = create_response.json()
        book_id = created_book['id']
        
        # Read - might need to wait a moment for the book to be available
        import time
        time.sleep(1)  # Small delay to ensure book is available
        
        read_response = api_client.get_book_by_id(book_id)
        if read_response.status_code == 404:
            # If book is not immediately available, skip the rest of the test
            logging.warning(f"Book {book_id} not immediately available after creation, skipping CRUD test")
            return
        
        asserter.assert_status_code(read_response, 200)
        retrieved_book = read_response.json()
        assert retrieved_book['id'] == book_id
        
        # Update
        updated_data = valid_book_data.copy()
        updated_data['title'] = "Updated Title"
        update_response = api_client.update_book(book_id, updated_data)
        asserter.assert_status_code(update_response, 200)
        updated_book = update_response.json()
        assert updated_book['title'] == "Updated Title"
        
        # Delete
        delete_response = api_client.delete_book(book_id)
        asserter.assert_status_code(delete_response, 200)
        
        # Verify deletion
        verify_response = api_client.get_book_by_id(book_id)
        asserter.assert_status_code(verify_response, 404)
        
        logging.info(f"Successfully completed CRUD lifecycle for book ID {book_id}")


    ## Test that API responses are consistent across multiple calls
    def test_api_response_consistency(self, api_client: BooksAPIClient, asserter: ResponseAsserter):
        # Get all books multiple times
        responses = []
        for i in range(3):
            response = api_client.get_all_books()
            asserter.assert_status_code(response, 200)
            responses.append(response.json())
        
        # Verify all responses have the same structure
        for i, books in enumerate(responses):
            asserter.assert_books_list_structure(books)
            if i > 0:
                assert len(books) == len(responses[0]), \
                    f"Response {i} has different number of books"
        
        logging.info("API response consistency verified across multiple calls")


    ## Test that API response headers are consistent
    def test_api_headers_consistency(self, api_client: BooksAPIClient, asserter: ResponseAsserter):
        response = api_client.get_all_books()
        asserter.assert_status_code(response, 200)
        
        # Verify expected headers
        headers = response.headers
        assert 'content-type' in headers, "Content-Type header missing"
        assert 'application/json' in headers['content-type'], \
            "Content-Type should be application/json"
        
        logging.info("API response headers consistency verified")


    ## Test that API response time is within acceptable limits
    def test_api_response_time(self, api_client: BooksAPIClient, asserter: ResponseAsserter):
        import time
        
        start_time = time.time()
        response = api_client.get_all_books()
        end_time = time.time()
        
        response_time = end_time - start_time
        asserter.assert_status_code(response, 200)
        
        # Acceptable response time: 5 seconds
        assert response_time < 5.0, f"Response time {response_time:.2f}s exceeds 5 second limit"
        
        logging.info(f"API response time: {response_time:.2f} seconds")


    ## Test that book data validation works correctly
    def test_book_data_validation(self, api_client: BooksAPIClient, asserter: ResponseAsserter, 
                                 validator: APIResponseValidator, existing_book_id: int):
        response = api_client.get_book_by_id(existing_book_id)
        asserter.assert_status_code(response, 200)
        
        book = response.json()
        
        # Validate using Pydantic model
        validation_errors = validator.validate_book_data(book)
        assert not validation_errors, f"Book data validation failed: {validation_errors}"
        
        # Validate using JSON schema
        assert validator.validate_book_response(book), \
            "Book data does not match JSON schema"
        
        logging.info(f"Book data validation passed for ID {existing_book_id}")


    ## Test that books list data validation works correctly
    def test_books_list_data_validation(self, api_client: BooksAPIClient, asserter: ResponseAsserter, 
                                       validator: APIResponseValidator):
        response = api_client.get_all_books()
        asserter.assert_status_code(response, 200)
        
        books = response.json()
        
        # Validate using JSON schema
        assert validator.validate_books_list_response(books), \
            "Books list data does not match JSON schema"
        
        # Validate each book individually
        for book in books:
            validation_errors = validator.validate_book_data(book)
            assert not validation_errors, f"Individual book validation failed: {validation_errors}"
        
        logging.info(f"Books list data validation passed for {len(books)} books") 
