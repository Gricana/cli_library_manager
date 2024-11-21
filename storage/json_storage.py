import json
import os
from typing import Dict, List, Optional, Generator, Any

from models.book import Book
from storage.exceptions import InvalidJsonFormatException
from storage.interface import BookStorage
from storage.observer import ObservableList


class JsonStorage(BookStorage):
    """
    A class for working with JSON storage of data about books.

    Implements the `BookStorage` interface
    and uses generators to work with data.
    """

    def __init__(self, file_path: str):
        """
        Initializing the storage.

        :param file_path: Path to the JSON file where the data is stored.
        """
        self.file_path = file_path
        self._ensure_file_exists()
        self.__books = ObservableList(
            list(self._load_books()), on_change=self._on_change
        )
        self.__index = self._create_index(self.__books)

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

    def _load_books(self) -> Generator[Book, Any, None]:
        """
        Load books from a JSON file as a generator.

        :return: Book object generator.
        :raises InvalidJsonFormatException: If the JSON file format is incorrect.
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                for book_data in data:
                    yield Book.from_json(book_data)
        except json.JSONDecodeError as e:
            raise InvalidJsonFormatException(f"Failed to parse JSON file: {e}")

    def _save_books(self) -> None:
        """
        Save changes to a JSON file.

        :return: None
        """
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                [book.to_json() for book in self.__books],
                file,
                ensure_ascii=False,
                indent=4
            )

    def _ensure_file_exists(self) -> None:
        """
        Verify that the JSON file exists.

        If the file does not exist, an empty file is created.
        """
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([], file)

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
        self._save_books()
