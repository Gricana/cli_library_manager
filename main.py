from cli.decorators import manage_history
from cli.parser import CLIParser
from manager.manage import BookManager
from storage.json_storage import JsonStorage


@manage_history()
def main():
    """
    The main function for launching the CLI application that manages the library.

    Loads the book store from a JSON file, initializes the book manager, and
    CLI parser for processing commands.

    If command line arguments are passed, the corresponding command is executed,
    otherwise, the CLI interactive mode is started.
    """

    # Initializing the book storage with a data file
    book_storage = JsonStorage(file_path="data/books.json")

    # Initializing a manager to work with books
    book_manager = BookManager(book_storage)

    # Initializing the CLI parser to process commands
    cli = CLIParser(book_manager)

    # Проверка наличия аргументов командной строки
    import sys
    if len(sys.argv) > 1:
        cli.execute_command(" ".join(sys.argv[1:]))
    else:
        # If there are no arguments, launch the interactive menu
        print("Welcome to the Library Manager CLI!")
        print("You can manage your library by typing commands.")
        print("Type 'exit' to quit the program.")

        while True:
            try:
                # Prompt for a command from the user
                command_input = input("> ")

                # Processing the exit command
                if command_input.lower() == "exit":
                    print("Exiting program...")
                    break

                # Executing the entered command
                cli.execute_command(command_input)
            except KeyboardInterrupt:
                # Handling a program interrupt from the keyboard
                print("\nUse 'exit' to quit the program.")
            except EOFError:
                # Error handling when input is complete
                print("\nExiting program...")
                break


if __name__ == "__main__":
    main()
