## API client module for making HTTP requests to the Books API.

import requests
import logging
from typing import Dict, Any
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from config.config import Config


## Generic HTTP client with retry logic and session management
class APIClient:
    
    ## Initialize the API client
    def __init__(self, timeout: int = None, max_retries: int = None):
        self.timeout = timeout or Config.API_TIMEOUT
        self.max_retries = max_retries or Config.MAX_RETRIES
        
        # Create session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=self.max_retries,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"],
            backoff_factor=Config.RETRY_DELAY
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        logging.info(f"API client initialized with timeout={self.timeout}s, max_retries={self.max_retries}")


    ## Make a GET request
    def get(self, url: str, params: Dict[str, Any] = None, headers: Dict[str, str] = None) -> requests.Response:
        return self._make_request('GET', url, params=params, headers=headers)


    ## Make a POST request
    def post(self, url: str, data: Dict[str, Any] = None, headers: Dict[str, str] = None) -> requests.Response:
        return self._make_request('POST', url, json=data, headers=headers)


    ## Make a PUT request
    def put(self, url: str, data: Dict[str, Any] = None, headers: Dict[str, str] = None) -> requests.Response:
        return self._make_request('PUT', url, json=data, headers=headers)


    ## Make a DELETE request
    def delete(self, url: str, headers: Dict[str, str] = None) -> requests.Response:
        return self._make_request('DELETE', url, headers=headers)



    ## Make an HTTP request with logging and error handling
    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        try:
            logging.debug(f"Making {method} request to {url}")
            
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )
            
            logging.debug(f"Response status: {response.status_code}")
            logging.debug(f"Response headers: {dict(response.headers)}")
            
            if response.status_code >= 400:
                logging.warning(f"Request failed with status {response.status_code}: {response.text}")
            else:
                logging.debug(f"Request successful: {response.status_code}")
            
            return response
            
        except requests.exceptions.Timeout:
            logging.error(f"Request timeout for {method} {url}")
            raise
        except requests.exceptions.ConnectionError:
            logging.error(f"Connection error for {method} {url}")
            raise
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error for {method} {url}: {e}")
            raise



## Specialized client for the Books API endpoints
class BooksAPIClient(APIClient):
    
    ## Initialize the Books API client
    def __init__(self):
        super().__init__()
        self.books_endpoint = Config.get_books_endpoint()
        logging.info(f"Books API client initialized with endpoint: {self.books_endpoint}")


    ## Get all books from the API
    def get_all_books(self) -> requests.Response:
        logging.info("Retrieving all books")
        return self.get(self.books_endpoint)


    ## Get a specific book by ID
    def get_book_by_id(self, book_id: int) -> requests.Response:
        url = Config.get_book_by_id_endpoint(book_id)
        logging.info(f"Retrieving book with ID: {book_id}")
        return self.get(url)


    ## Create a new book
    def create_book(self, book_data: Dict[str, Any]) -> requests.Response:
        logging.info(f"Creating book with title: {book_data.get('title', 'Unknown')}")
        return self.post(self.books_endpoint, data=book_data)


    ## Update an existing book
    def update_book(self, book_id: int, book_data: Dict[str, Any]) -> requests.Response:
        url = Config.get_book_by_id_endpoint(book_id)
        logging.info(f"Updating book with ID: {book_id}")
        return self.put(url, data=book_data)


    ## Delete a book
    def delete_book(self, book_id: int) -> requests.Response:
        url = Config.get_book_by_id_endpoint(book_id)
        logging.info(f"Deleting book with ID: {book_id}")
        return self.delete(url) 
