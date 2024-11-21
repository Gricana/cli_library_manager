from dataclasses import dataclass, field, asdict
from typing import Dict

from models.constants import BookStatus
from models.exceptions import ValidationException
from models.utils import generate_unique_id
from models.validators.book import BookValidator


@dataclass
class Book:
    """
    Book model class.

    Represents a book with the fields: id, title, author, year, status.
    Includes methods for object serialization, validation,
    and creating a unique identifier.
    """

    id: str = field(init=False)
    title: str
    author: str
    year: int
    status: str = field(default=BookStatus.AVAILABLE.value)

    def __post_init__(self):
        """
        Initializing a book instance.

        If the object does not contain an ID, a unique identifier is generated.
        """
        if not hasattr(self, 'id') or not self.id:
            self.id = generate_unique_id()

    def to_dict(self) -> dict:
        """
        Converts a book object to a dictionary.

        :return: A dict containing the book data.
        """
        return asdict(self)

    def to_json(self) -> dict:
        """
        Converts a book object into a dict for JSON.

        :return: A dict with book data,
                 including a string representation of the status.
        """
        book_data = self.to_dict()
        book_data['status'] = self.status
        return book_data

    @classmethod
    def from_json(cls, data: Dict) -> "Book":
        """
        Creates a Book object from JSON data.

        :param data: Book data in the form of a dict (or JSON).
        :return: An object of the `Book` class.
        """
        book = cls(
            title=data.get("title"),
            author=data.get("author"),
            year=data.get("year"),
            status=data.get("status", ""),
        )
        book.id = data["id"]
        return book

    def validate(self) -> bool:
        """
        The validity of the data is checked after the creation of the object,
        if any changed.

        :return: `True` if the book passed validation,
                  otherwise throws an exception.
        :raises ValidationException: If the book data is invalid.
        """
        validator = BookValidator()
        try:
            validator.validate_data(self.to_dict())
            return True
        except ValidationException as e:
            raise e
