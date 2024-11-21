class ValidationException(Exception):
    """
    An exception that is thrown when the validation data does not match.
    """
    pass


class BookNotFoundException(Exception):
    """
    The exception that is thrown when the book is not found.

    This exception is used when searching for a book by ID is unsuccessful.
    """
    pass
