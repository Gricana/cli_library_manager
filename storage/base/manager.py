from abc import ABC, abstractmethod
from typing import List, Optional

from models.book import Book


class StorageManager(ABC):
    """
    Interface for managing storage of books.

    This interface provides the basic CRUD-operations
    for working with books in a storage.
    The implementation of these operations will vary based
    on the underlying data storage mechanism (e.g., file system, database, etc.).
    """

    @abstractmethod
    def save(self, book: Book) -> None:
        """
        Saves the book to the storage.

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

    @abstractmethod
    def _load_objs(self) -> List[Book]:
        """
        Loads book objects from the storage.

        This method should be implemented by concrete classes
        to load data from the underlying source.
        """
        pass

    def _save_objs(self) -> None:
        """
        Saves book objects to the storage.

        This method should be implemented by concrete classes
        to save data to the underlying source.
        """
        pass
