from typing import Dict, List, Optional

from models.book import Book
from storage.base.manager import StorageManager
from storage.base.observer import ObservableList
from storage.base.source import DataSource


class BookStorageManager(StorageManager):
    """
    A class for working with storage of data about books.

    Implements the `StorageManager` interface
    and provides functionality to manage books,
    including CRUD operations over the books.
    This implementation uses generators to load and save book data.
    """

    def __init__(self, data_source: DataSource):
        """
        Initializes the book storage.

        :param data_source: The data source used to load and save books.
        """
        self.data_source = data_source
        self.__books = ObservableList(
            list(self._load_objs()), on_change=self._on_change
        )
        self.__index = self._create_index(self.__books)

    def _load_objs(self) -> List[Book]:
        """
        Loads books from the data source.

        :return: A list of Book objects loaded from the data source.
        """
        return [Book.from_json(data) for data in self.data_source.load()]

    def _save_objs(self) -> None:
        """
        Saves the books to the data source.

        :return: None
        """
        self.data_source.save([book.to_json() for book in self.__books])

    def save(self, book: Book) -> None:
        """
        Save or update book information.

        :param book: Book object to save.
        """
        found = False
        # Update a Book if it already exists
        for i, b in enumerate(self.__books):
            if b.id == book.id:
                self.__books[i] = book
                found = True
                break

        if not found:
            self.__books.append(book)

    def get(self, book_id: str) -> Optional[Book]:
        """
        Get a book by its ID.

        :param book_id: Unique identifier of the book.
        :return: Found book object or None.
        """
        for book in self.__books:
            if book.id == book_id:
                return book
        return None

    def delete(self, book: Book) -> None:
        """
        Remove a book from storage.

        :param book: The book object to delete.
        """
        self.__books.remove(book)

    def find(self, query: Optional[str]) -> List[Book]:
        """
        Find books based on a given query.

        :param query: Search string. Compares with title, author and year.
        :return: List of book objects matching the request.
        """
        if query:
            query = query.lower()
            result_ids = set()

            # Search by fields: title, author, year
            for field in ['title', 'author', 'year']:
                for value in self.__index[field].keys():
                    if query in value:
                        result_ids.update(self.__index[field][value])

            return [book for book in self.__books if book.id in result_ids]

        return self.__books

    def all(self) -> List[Book]:
        """
        Get a list of all books.

        :return: List of book objects.
        """
        return self.__books

    def _create_index(self, books: List[Book]) -> Dict[str, Dict[str, set]]:
        """
        Create an index to quickly search books by field.

        :param books: List of book objects.
        :return: A dictionary containing an index of books by field.
        """
        index = {
            "title": {},
            "author": {},
            "year": {}
        }

        def add_to_index(field: str, value: str, book_id: str) -> None:
            """
            Add a value to the index.

            :param field: Field for indexing (title, author, year).
            :param value: Value to index.
            :param book_id: Unique identifier of the book.
            """
            value = value.lower()
            if value not in index[field]:
                index[field][value] = set()
            index[field][value].add(book_id)

        # Indexing books by field
        for book in books:
            add_to_index("title", book.title, book.id)
            add_to_index("author", book.author, book.id)
            add_to_index("year", str(book.year), book.id)

        return index

    def _on_change(self) -> None:
        """
        Update the index and save books to a file when data changes.

        :return: None
        """
        self.__index = self._create_index(self.__books)
        self._save_objs()
