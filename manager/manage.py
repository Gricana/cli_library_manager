from typing import List, Optional

from models.book import Book
from models.constants import BookStatus
from models.exceptions import ValidationException, BookNotFoundException
from storage.interface import BookStorage


class BookManager:
    """
    Book management class.

    This class provides methods for adding, removing,
    searching and updating books in the repository.
    """

    def __init__(self, book_storage: BookStorage):
        """
        Initializes BookManager with a book store.

        :param book_storage: A book storage instance
                             that implements the BookStorage interface.
        """
        self.book_storage = book_storage

    def add_book(self, book: Book) -> None:
        """
        Adds a book to storage.

        :param book: A copy of the book to add.
        :raises ValidationException: If the book data is not validated.
        """
        if not book.validate():
            raise ValidationException("Book data is invalid.")
        self.book_storage.save(book)

    def remove_book(self, book_id: str) -> None:
        """
        Removes a book from storage by its ID.

        :param book_id: ID of the book to delete.
        :raises BookNotFoundException: If the book with the given ID is not found.
        """
        book = self.book_storage.get(book_id)
        if not book:
            raise BookNotFoundException(f"Book with ID {book_id} not found")
        self.book_storage.delete(book)

    def find_books(self, query: Optional[str] = None) -> List[Book]:
        """
        Searches for books by title, author or year of publication.

        :param query: Query string for searching by book fields.
        :return: List of books that satisfy the request.
        """
        return self.book_storage.find(query)

    def update_status(self, book_id: str, status: str) -> None:
        """
        Updates the status of a book.

        :param book_id: ID of the book to update the status.
        :param status: New status of the book.
        :raises BookNotFoundException: If the book with the given ID is not found.
        :raises ValidationException: If an invalid status is passed.
        """
        book = self.book_storage.get(book_id)
        if not book:
            raise BookNotFoundException(f"Book with ID {book_id} not found")

        if status not in BookStatus:
            raise ValidationException(f"Invalid status: {status}")

        book.status = status
        self.book_storage.save(book)

    def all(self) -> List[Book]:
        """
        Returns a list of all books in the repository.

        :return: List of all books.
        """
        return self.book_storage.all()
