import os
import readline
from typing import Callable


def manage_history(file: str = ".library_cli_history", length: int = 100):
    """
    A decorator for managing command history on the CLI
    and saving it to a file.

    This decorator allows you to save and load command history from a file,
    and also set the length of the story.

    :param file: Path to the file where the command history will be saved.
    The default is `.library_cli_history`.
    :param length: The maximum length of the command history. Default is 100.
    :raises FileNotFoundError: If the history file is not found when attempting to load.
    :raises Exception: Possible other errors when reading or writing to the history file.
    """

    def decorator(func: Callable):
        """
        A decorator that adds history control to a command line function.

        :param func: A function that will be wrapped by a decorator.
        :return: Wrapped function with functionality for loading and saving command history.
        """

        def wrapper(*args, **kwargs):
            try:
                # Load command history from a file, if the file exists
                if os.path.exists(file):
                    readline.read_history_file(file)
            except FileNotFoundError:
                # If the file is not found, ignore the error
                print(
                    f"Warning: History file '{file}' not found. "
                    f"Creating a new one.")
            except Exception as e:
                print(f"Error reading history file: {e}")

            readline.set_history_length(length)

            try:
                # Execute the original function
                result = func(*args, **kwargs)
            finally:
                try:
                    readline.write_history_file(file)
                except Exception as e:
                    print(f"Error writing history file: {e}")

            return result

        return wrapper

    return decorator
