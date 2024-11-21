from typing import List, Optional

from models.book import Book


class BookStorage:
    """
    Storage interface for managing books.

    This class describes the basic operations with books in the repository,
    such as adding, deleting, searching, updating status and getting all books.
    """

    def save(self, book: Book) -> None:
        """
        Saves the book to storage.

        :param book: The Book object to save.
        """
        pass

    def get(self, book_id: str) -> Optional[Book]:
        """
        Retrieves a Book by ID.

        :param book_id: Identifier of the Book to be retrieved.
        :return: Book with the specified ID, or None if the Book is not found.
        """
        pass

    def delete(self, book: Book) -> None:
        """
        Removes a Book from storage.

        :param book: The Book to be deleted.
        """
        pass

    def find(self, query: Optional[str]) -> List[Book]:
        """
        Searches for books based on a given query.

        :param query: Query for searching books. Maybe by title, author, year.
        :return: List of books matching the request.
        """
        pass

    def update_status(self, book_id: str, new_status: str) -> None:
        """
        Updates the status of a Book.

        :param book_id: Identifier of the Book
                        whose status needs to be updated.
        :param new_status: New status of the book.
        """
        pass

    def all(self) -> List[Book]:
        """
        Retrieves all books from the storage.

        :return: List of all books.
        """
        pass
