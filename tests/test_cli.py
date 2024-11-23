import os
import unittest
from io import StringIO
from unittest.mock import patch

from cli.parser import CLIParser
from manager.manage import BookManager
from models.book import Book
from models.constants import BookStatus
from storage.json.manager import BookStorageManager
from storage.json.source import JsonSource


class TestCLIParser(unittest.TestCase):
    def setUp(self):
        self.test_file_path = 'data/books.json'
        self.book_source = JsonSource(self.test_file_path)
        self.book_storage = BookStorageManager(self.book_source)
        self.book_manager = BookManager(self.book_storage)
        self.cli_parser = CLIParser(self.book_manager)

    def tearDown(self):
        """
        Performed after each test.
        Clears the data file in preparation for the next test.
        """
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    @patch("sys.stdout", new_callable=StringIO)
    def test_add_book(self, mock_stdout):
        # Command to add a book
        command_input = ("add-book 'The Great Gatsby' 'F. Scott Fitzgerald' "
                         "1925")

        # Executing a command
        self.cli_parser.execute_command(command_input)

        self.assertIn("Book 'The Great Gatsby' added successfully.",
                      mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_show_all_books_table_format(self, mock_stdout):
        """
        Test to check the output of books in table format.
        """
        # Adding books via BookManager
        self.book_manager.add_book(
            Book(title="1984", author="George Orwell", year=1949))
        self.book_manager.add_book(
            Book(title="Brave New World", author="Aldous Huxley", year=1932))

        # Execute a command via CLIParser
        command_input = "show-all"
        self.cli_parser.execute_command(command_input)

        # Checking the contents of the table
        output = mock_stdout.getvalue()
        self.assertRegex(output,
                         r"1984\s+\|\s+George Orwell\s+\|\s+1949\s+\|\s+в наличии")
        self.assertRegex(output, r"Brave New World\s+\|\s+Aldous "
                                 r"Huxley\s+\|\s+1932\s+\|\s+в наличии")

        # Let's make sure each line starts with ID
        for line in output.split("\n"):
            if "|" in line and not line.startswith("ID"):
                self.assertRegex(line, r"^[a-f0-9\-]{36}\s+\|")

    @patch("sys.stdout", new_callable=StringIO)
    def test_find_books(self, mock_stdout):

        # Adding books
        self.book_manager.add_book(
            Book(title="1984", author="George Orwell", year=1949))
        self.book_manager.add_book(
            Book(title="Brave New World", author="Aldous Huxley", year=1932))

        # Command to search for "1984"
        command_input = "find-books 1984"

        # Executing a command
        self.cli_parser.execute_command(command_input)

        # Checking that the book "1984" is displayed
        self.assertIn("1984", mock_stdout.getvalue())
        self.assertNotIn("Brave New World", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_update_status(self, mock_stdout):
        # Adding a book
        book = Book(title="1984", author="George Orwell", year=1949)
        self.book_manager.add_book(book)

        # Command to update book status
        command_input = f"update-status {book.id} выдана"

        # Executing a command
        self.cli_parser.execute_command(command_input)

        # Checking that the book's status has been updated
        updated_book = self.book_manager.all()[0]
        self.assertEqual(updated_book.status, BookStatus.ISSUED.value)
        self.assertIn(
            f"Status of book with ID {book.id} updated to 'выдана'.",
            mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_remove_book(self, mock_stdout):
        # Add a book
        book = Book(title="1984", author="George Orwell", year=1949)
        self.book_manager.add_book(book)

        # Command to delete a book
        command_input = f"remove-book {book.id}"

        # Executing a command
        self.cli_parser.execute_command(command_input)

        # Verifying that a book has been deleted
        self.assertEqual(len(self.book_manager.all()), 0)
        self.assertIn(f"Book with ID {book.id} removed successfully.",
                      mock_stdout.getvalue())

    @patch("sys.stderr", new_callable=StringIO)
    def test_add_book_missing_quotes_error(self, mock_stderr):
        """
        Test for trying to add a Book with missing quotes
        for values with spaces.
        """
        # Command to add book without quotes around values with spaces
        command_input = "add-book The Great Gatsby F. Scott Fitzgerald 1925"

        # Executing a command
        self.cli_parser.execute_command(command_input)

        # Retrieving the usage message from stderr
        error_message = mock_stderr.getvalue()

        # Checking that the output contains error description
        self.assertIn("add-book: error: argument ", error_message)

    @patch("sys.stderr", new_callable=StringIO)
    def test_invalid_command(self, mock_stderr):
        """
        Test for entering an unknown command.
        """
        # Invalid command
        command_input = "random-book"

        # Executing a command
        self.cli_parser.execute_command(command_input)

        # Retrieve the usage message from stderr
        error_message = mock_stderr.getvalue()

        # Checking that the output contains an error about an unknown command
        self.assertIn("error: argument command: invalid choice:",
                      error_message)

    @patch("sys.stdout", new_callable=StringIO)
    def test_no_command(self, mock_stdout):
        """
        Test for lack of command.
        """
        # Empty input
        command_input = ""

        # Executing a command
        self.cli_parser.execute_command(command_input)

        # Retrieving the message from stdout
        error_message = mock_stdout.getvalue()

        # Checking for missing command
        self.assertIn("No command provided.", error_message)
        self.assertIn("Use 'help' for a list of commands.", error_message)


if __name__ == '__main__':
    unittest.main()
