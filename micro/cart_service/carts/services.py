import requests
from django.conf import settings


class BookServiceClient:
    """Client to communicate with Book Service"""
    
    def __init__(self):
        self.base_url = settings.BOOK_SERVICE_URL

    def get_book(self, book_id):
        """
        Get book details from Book Service
        Returns: dict with book data or None if not found
        """
        try:
            response = requests.get(f"{self.base_url}/api/books/{book_id}/", timeout=5)
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Book Service: {e}")
            return None

    def check_stock(self, book_id, quantity):
        """
        Check if book has sufficient stock
        Returns: dict with availability info or None if error
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/books/{book_id}/check-stock/",
                params={'quantity': quantity},
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error checking stock: {e}")
            return None

    def get_books_by_ids(self, book_ids):
        """
        Get multiple books by IDs
        Returns: list of book data
        """
        books = []
        for book_id in book_ids:
            book = self.get_book(book_id)
            if book:
                books.append(book)
        return books
