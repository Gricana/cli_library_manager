import os
import unittest

from models.book import Book
from storage.exceptions import InvalidJsonFormatException
from storage.json_storage import JsonStorage


class TestJsonStorage(unittest.TestCase):

    def setUp(self):
        """
        Performed before each test.
        We create a test storage with a temporary file.
        """
        self.test_file_path = "data/test_books.json"
        self.storage = JsonStorage(file_path=self.test_file_path)

    def tearDown(self):
        """
        Performed after each test.
        Clears the data file in preparation for the next test.
        """
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_create_storage(self):
        """
        Verifies that when a JsonStorage object is created, a file is created.
        """
        self.assertTrue(os.path.exists(self.test_file_path))

    def test_add_book_to_storage(self):
        """
        Checks whether a book has been added to the storage.
        """
        book = Book(title="Test Book", author="Author", year=2024)
        self.storage.save(book)

        # Checking that the book has been added
        books = self.storage.all()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Test Book")
        self.assertTrue(books[0].id)

    def test_get_all_books_empty(self):
        """
        Checks that the all method returns an empty list if the file is empty.
        """
        books = self.storage.all()
        self.assertEqual(len(books), 0)

    def test_get_book_by_id(self):
        """
        Checks that the book can be found by ID.
        """
        book = Book(title="Test Book", author="Author", year=2024)
        self.storage.save(book)

        # Check that the book is found by ID
        retrieved_book = self.storage.get(book.id)
        self.assertEqual(retrieved_book.title, "Test Book")

    def test_get_book_by_non_existing_id(self):
        """
        Checks that the get_book_by_id method throws an exception
        when trying to find a book with a non-existent ID.
        """

        self.assertIsNone(
            self.storage.get("3bb236a3-5de3-467a-8502-7b4510d30c51")
        )

    def test_remove_book(self):
        """
        Checks the deletion of a book from storage and checks for file changes.
        """
        book = Book(title="Test Book", author="Author", year=2024)
        self.storage.save(book)

        # Checking that the book has been added
        storage_after_save = JsonStorage(file_path=self.test_file_path)
        books_after_save = storage_after_save.all()
        self.assertEqual(len(books_after_save), 1)
        self.assertEqual(books_after_save[0].title, "Test Book")

        # Deleting a book
        self.storage.delete(book)

        # Create a new JsonStorage object
        # and check that the book has been deleted
        storage_after_delete = JsonStorage(file_path=self.test_file_path)
        books_after_delete = storage_after_delete.all()
        self.assertEqual(len(books_after_delete), 0)

    def test_update_book(self):
        """
        Checks whether the Book data is updated in the storage.
        """
        book = Book(title="Test Book", author="Author", year=2024)
        self.storage.save(book)

        # Updating information about the book
        book.title = "Updated Book"
        self.storage.save(book)

        # Checking that the book has been updated
        updated_book = self.storage.get(book.id)
        self.assertEqual(updated_book.title, "Updated Book")

    def test_empty_file(self):
        """
        Checks correct operation with an empty file.
        """
        # Create an empty file
        with open(self.test_file_path, 'w') as f:
            f.write('[]')

        books = self.storage.all()
        self.assertEqual(len(books), 0)

    def test_invalid_json_format(self):
        """
        Checks that if the file is corrupted, an error is thrown
        when attempting to load data.
        """
        with open(self.test_file_path, 'w') as f:
            f.write('{"title": 123')  # Invalid JSON format

        with self.assertRaises(InvalidJsonFormatException):
            JsonStorage(self.test_file_path)

    def test_overwrite_file(self):
        """
        Checks that when new data is added, the file is actually overwritten.
        """
        # Create the first book and save it
        book1 = Book(title="Test Book 1", author="Author 1", year=2024)
        self.storage.save(book1)

        # Create a new JsonStorage object and check the contents of the file
        storage_after_first_save = JsonStorage(file_path=self.test_file_path)
        books_after_first_save = storage_after_first_save.all()
        self.assertEqual(len(books_after_first_save), 1)
        self.assertEqual(books_after_first_save[0].title, "Test Book 1")

        # Add a second book and save it
        book2 = Book(title="Test Book 2", author="Author 2", year=2024)
        self.storage.save(book2)

        # Create a new JsonStorage object
        # and check that the file is overwritten correctly
        storage_after_second_save = JsonStorage(file_path=self.test_file_path)
        books_after_second_save = storage_after_second_save.all()
        self.assertEqual(len(books_after_second_save), 2)
        self.assertEqual(books_after_second_save[0].title, "Test Book 1")
        self.assertEqual(books_after_second_save[1].title, "Test Book 2")


if __name__ == "__main__":
    unittest.main()
