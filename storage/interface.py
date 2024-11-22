from abc import ABC, abstractmethod
from typing import List, Optional

from models.book import Book


class BookStorage(ABC):
    """
    Storage interface for managing books.

    This class describes the basic operations with books in the repository,
    such as adding, deleting, searching, updating status and getting all books.
    """

    @abstractmethod
    def save(self, book: Book) -> None:
        """
        Saves the book to storage.

        :param book: The Book object to save.
        """
        pass

    @abstractmethod
    def get(self, book_id: str) -> Optional[Book]:
        """
        Retrieves a Book by ID.

        :param book_id: Identifier of the Book to be retrieved.
        :return: Book with the specified ID, or None if the Book is not found.
        """
        pass

    @abstractmethod
    def delete(self, book: Book) -> None:
        """
        Removes a Book from storage.

        :param book: The Book to be deleted.
        """
        pass

    @abstractmethod
    def find(self, query: Optional[str]) -> List[Book]:
        """
        Searches for books based on a given query.

        :param query: Query for searching books. Maybe by title, author, year.
        :return: List of books matching the request.
        """
        pass

    @abstractmethod
    def all(self) -> List[Book]:
        """
        Retrieves all books from the storage.

        :return: List of all books.
        """
        pass
