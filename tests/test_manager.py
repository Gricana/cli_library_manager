import os
import unittest

from manager.manage import BookManager
from models.book import Book
from models.constants import BookStatus
from models.exceptions import BookNotFoundException, ValidationException
from storage.json.manager import BookStorageManager
from storage.json.source import JsonSource


class TestBookManager(unittest.TestCase):

    def setUp(self):
        """
        Performed before each test.
        A temporary storage for tests is created.
        """
        # The path to the test file
        self.test_file_path = "data/test_books.json"

        # Create temporary storage for tests
        self.source = JsonSource(self.test_file_path)
        self.storage = BookStorageManager(self.source)
        self.book_manager = BookManager(self.storage)

    def tearDown(self):
        """
        Performed after each test.
        Clears the data file in preparation for the next test.
        """
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_add_book(self):
        """
        Checks whether a book has been added to the repository.
        """
        book = Book(title="Test Book", author="Author", year=2024)
        self.book_manager.add_book(book)
        books = self.book_manager.all()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, book.title)
        self.assertTrue(books[0].id)

    def test_remove_book(self):
        """
        Checks book deletion by ID.
        """
        book = Book(title="Test Book", author="Author", year=2024)
        self.book_manager.add_book(book)
        self.book_manager.remove_book(book.id)
        books = self.book_manager.all()
        self.assertEqual(len(books), 0)

    def test_find_books(self):
        """
        Checks the search for a book by part of the title.
        """
        book = Book(title="Test Book", author="Author", year=2024)
        self.book_manager.add_book(book)
        books = self.book_manager.find_books("Test")
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, book.title)

    def test_update_status(self):
        """
        Checks for changes in book status.
        """
        book = Book(title="Test Book", author="Author", year=2024)
        self.book_manager.add_book(book)
        self.book_manager.update_status(book.id, BookStatus.ISSUED.value)
        updated_book = self.book_manager.all()[0]
        self.assertEqual(updated_book.status, BookStatus.ISSUED.value)

    def test_update_status_book_not_found(self):
        """
        Checks that an exception will be thrown
        if we try to update the status of a book with a non-existent ID.
        """
        with self.assertRaises(BookNotFoundException):
            self.book_manager.update_status(
                "eb55d06a-23e7-451c-998c-598e366cf82b",  # Non-existent ID
                BookStatus.ISSUED.value)

    def test_remove_book_not_found(self):
        """
        Checks that an exception will be thrown
        if we try to delete a book with a non-existent ID.
        """
        with self.assertRaises(BookNotFoundException):
            self.book_manager.remove_book(
                "0a2dbc59-e9d0-4391-afb1-93380fb348d5"  # Non-existent ID
            )

    def test_update_status_invalid(self):
        """
        Checks that an exception will be thrown
        if we try to set an invalid status.
        """
        book = Book(title="Test Book", author="Author", year=2024)
        self.book_manager.add_book(book)
        with self.assertRaises(ValidationException):
            self.book_manager.update_status(book.id, "утрачена")  # Invalid status

    def test_no_books_in_storage(self):
        """
        Checks that the `all()` method returns an empty list
        if there are no books.
        """
        books = self.book_manager.all()
        self.assertEqual(len(books), 0)


if __name__ == "__main__":
    unittest.main()
