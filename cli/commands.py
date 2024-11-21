from abc import ABC, abstractmethod
from dataclasses import fields
from typing import List

from manager.manage import BookManager
from models.book import Book


class Command(ABC):
    """
    Abstract class for all commands.
    Every command must implement an `execute` method.
    """

    @abstractmethod
    def execute(self, args):
        """
        Executes the command.

        :param args: The parameters the command uses to execute.
        """
        pass


class ShowAllCommand(Command):
    """
    Command to display all books.

    This class uses `BookManager` to get all the books
    and display them in a table.
    """

    def __init__(self, book_manager: BookManager):
        """
        Initializes a command to display all books.

        :param book_manager: A `BookManager` object that manages books.
        """
        self.book_manager = book_manager

    def _get_book_headers(self) -> List[str]:
        """
        Gets a list of headers for a table from the fields of the `Book` model.

        :return: List of lines with headers.
        """
        return [field.name.upper() for field in fields(Book)]

    def _print_table(self, books: List[Book]) -> None:
        """
        Displays a table of all books.

        :param books: List of Book objects.
        """
        headers = self._get_book_headers()
        column_widths = {header: len(header) for header in headers}
        book_data = [book.to_json() for book in books]

        for book in book_data:
            for header in headers:
                column_widths[header] = max(
                    column_widths[header],
                    len(str(book.get(header.lower(), "")))
                )

        # Displaying table headers
        header_row = " | ".join(
            header.ljust(column_widths[header]) for header in headers)
        print(header_row)
        print("-" * len(header_row))

        # Output of book data
        for book in book_data:
            row = " | ".join(
                str(book.get(header.lower(), "")).ljust(
                    column_widths[header]) for header in headers)
            print(row)

    def execute(self, args):
        """
        Executes the command to display all books.

        :param args: Parameters for executing the command.
        In this case, the parameters are not used.
        """
        try:
            books = self.book_manager.all()
            if books:
                self._print_table(books)
            else:
                print("No books available.")
        except Exception as e:
            print(f"Error: {e}")


class ShowFilteredBooksCommand(ShowAllCommand):
    """
    Command to display books that match the filter (on request).
    """

    def __init__(self, book_manager: BookManager):
        """
        Initializes the command to display filtered books.

        :param book_manager: A `BookManager` object that manages books.
        """
        super().__init__(book_manager)

    def execute(self, args):
        """
        Executes the command to display books that match the request.

        :param args: Command arguments that contain the query string to filter.
        """
        try:
            query = args.query.lower()
            books = self.book_manager.find_books(query)
            if books:
                self._print_table(books)
            else:
                print("No books found.")
        except Exception as e:
            print(f"Error: {e}")


class AddBookCommand(Command):
    """
    Command to add a new book.
    """

    def __init__(self, book_manager: BookManager):
        """
        Initializes the command to add a new book.

        :param book_manager: A `BookManager` object that manages books.
        """
        self.book_manager = book_manager

    def execute(self, args):
        """
        Executes the command to add a new book.

        :param args: Command arguments that contain information about the book.
        """
        try:
            # Create a new Book and add it to the storage
            book = Book(title=args.title, author=args.author,
                        year=args.year, status=args.status)
            self.book_manager.add_book(book)
            print(f"Book '{args.title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")


class RemoveBookCommand(Command):
    """
    Command to delete a book by ID.
    """

    def __init__(self, book_manager: BookManager):
        """
        Initiates a command to delete a workbook.

        :param book_manager: A `BookManager` object that manages books.
        """
        self.book_manager = book_manager

    def execute(self, args):
        """
        Executes the command to delete a Book.

        :param args: Command arguments that contain the ID of the book to delete.
        """
        try:
            self.book_manager.remove_book(args.book_id)
            print(f"Book with ID {args.book_id} removed successfully.")
        except Exception as e:
            print(f"Error: {e}")


class UpdateStatusCommand(Command):
    """
    Command to update the status of a book.
    """

    def __init__(self, book_manager: BookManager):
        """
        Initiates a command to update the Book status.

        :param book_manager: A `BookManager` object that manages books.
        """
        self.book_manager = book_manager

    def execute(self, args):
        """
        Executes the command to update the workbook status.

        :param args: Command arguments that contain the book ID and new status.
        """
        try:
            self.book_manager.update_status(args.book_id, args.status)
            print(f"Status of book with ID {args.book_id} "
                  f"updated to '{args.status}'.")
        except Exception as e:
            print(f"Error: {e}")
