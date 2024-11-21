import argparse
import shlex

from cli.commands import (AddBookCommand, UpdateStatusCommand,
                          RemoveBookCommand,
                          ShowAllCommand, ShowFilteredBooksCommand)
from manager.manage import BookManager
from models.constants import BookStatus


class CLIParser:
    def __init__(self, book_manager: BookManager):
        """
        Initializes the command line parser to manage the library.

        :param book_manager: A BookManager instance for managing books.
        """
        self.book_manager = book_manager
        self.parser = argparse.ArgumentParser(
            description="Library Manager CLI")
        self.subparsers = self.parser.add_subparsers(dest="command")

        self._add_add_book_command()
        self._add_show_all_command()
        self._add_update_status_command()
        self._add_remove_book_command()
        self._add_find_books_command()

    def _add_add_book_command(self):
        """Adds a command to add a book."""
        add_parser = self.subparsers.add_parser("add-book",
                                                help="Add a new book")
        add_parser.add_argument("title", type=str, help="Title of the book")
        add_parser.add_argument("author", type=str, help="Author of the book")
        add_parser.add_argument("year", type=int, help="Year of publication")
        add_parser.add_argument(
            "status", type=str,
            choices=BookStatus.get_status_choices(),
            nargs="?",
            default=BookStatus.AVAILABLE.value,
            help="Book status (default: available)"
        )

    def _add_show_all_command(self):
        """Adds a command to display all books."""
        self.subparsers.add_parser("show-all", help="Show all books")

    def _add_update_status_command(self):
        """Adds a command to change the status of a book."""
        update_parser = self.subparsers.add_parser("update-status",
                                                   help="Update book status")
        update_parser.add_argument("book_id", type=str, help="ID of the book")
        update_parser.add_argument(
            "status", type=str,
            choices=BookStatus.get_status_choices(),
            help="New status"
        )

    def _add_remove_book_command(self):
        """Adds a command to delete a book."""
        remove_parser = self.subparsers.add_parser("remove-book",
                                                   help="Remove a book")
        remove_parser.add_argument("book_id", type=str,
                                   help="ID of the book to remove")

    def _add_find_books_command(self):
        """Adds a command to search for books."""
        find_parser = self.subparsers.add_parser("find-books",
                                                 help="Find books")
        find_parser.add_argument("query", type=str, help="Search query")

    def execute_command(self, command_input: str):
        """
        Parses the command and performs the appropriate action.

        :param command_input: Command input string.
        """
        args = self._parse_command(command_input)
        if args is None or not args.command:
            print("No command provided. Use 'help' for a list of commands.")
            return

        command = self._get_command(args.command)
        if command:
            self._execute_command(command, args)
        else:
            print(f"Unknown command: {args.command}. "
                  f"Use 'help' for a list of commands.")

    def _parse_command(self, command_input: str):
        """
        Parses a command and returns arguments.

        :param command_input: Command string for parsing.
        :return: Object with arguments, or None on error.
        """
        try:
            return self.parser.parse_args(shlex.split(command_input))
        except SystemExit:
            return None

    def _get_command(self, command_name: str):
        """
        Returns the matching command by name.

        :param command_name: Command name.
        :return: Command object or None.
        """
        command_map = {
            "add-book": AddBookCommand(self.book_manager),
            "show-all": ShowAllCommand(self.book_manager),
            "update-status": UpdateStatusCommand(self.book_manager),
            "remove-book": RemoveBookCommand(self.book_manager),
            "find-books": ShowFilteredBooksCommand(self.book_manager),
        }
        return command_map.get(command_name)

    def _execute_command(self, command, args):
        """Executes a command."""
        command.execute(args)
