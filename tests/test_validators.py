import unittest
from datetime import datetime

from models.book import Book
from models.constants import BookStatus
from models.exceptions import ValidationException


class TestBookValidator(unittest.TestCase):
    def test_valid_book(self):
        """
        Checks for successful validation of a valid Book object.
        """
        book = Book(
            title="Valid Title",
            author="Valid Author",
            year=2023,
            status=BookStatus.AVAILABLE.value
        )
        self.assertTrue(book.validate())

    def test_missing_required_field_title(self):
        """
        Checks that the absence of a required field throws a ValidationException.
        """
        with self.assertRaises(ValidationException) as context:
            book = Book(
                title="",
                author="Valid Author",
                year=2023,
                status=BookStatus.AVAILABLE.value
            )
            book.validate()
        self.assertIn("Fields cannot be empty: title", str(context.exception))

    def test_invalid_data_type_year(self):
        """
        Checks that an invalid data type for year throws a ValidationException.
        """
        with self.assertRaises(ValidationException) as context:
            book = Book(
                title="Valid Title",
                author="Valid Author",
                year="Not a Year",  # Invalid type
                status=BookStatus.AVAILABLE.value
            )
            book.validate()
        self.assertIn("Field 'year' must be of type int",
                      str(context.exception))

    def test_empty_author_field(self):
        """
        Checks that an empty author field throws a ValidationException.
        """
        with self.assertRaises(ValidationException) as context:
            book = Book(
                title="Valid Title",
                author="   ",  # Empty string
                year=2023,
                status=BookStatus.AVAILABLE.value
            )
            book.validate()
        self.assertIn("Fields cannot be empty: author", str(context.exception))

    def test_invalid_status_choice(self):
        """
        Checks that an invalid status value throws a ValidationException.
        """
        with self.assertRaises(ValidationException) as context:
            book_data = {
                "id": "12345",
                "title": "Valid Title",
                "author": "Valid Author",
                "year": 2024,
                "status": "утрачена"  # Invalid status
            }
            book = Book.from_json(book_data)
            book.validate()
        self.assertEqual("Incorrect status: утрачена. "
                         "Valid values: ['в наличии', 'выдана']",
                         str(context.exception))

    def test_invalid_year_future(self):
        """
        Checks that the year in the future throws a ValidationException.
        """
        future_year = datetime.now().year + 1
        with self.assertRaises(ValidationException) as context:
            book = Book(
                title="Valid Title",
                author="Valid Author",
                year=future_year,  # Next year
                status=BookStatus.AVAILABLE.value
            )
            book.validate()
        self.assertIn(f"Year must be between 1 and {datetime.now().year}",
                      str(context.exception))

    def test_invalid_year_past(self):
        """
        Checks that the year is too small and throws a ValidationException.
        """
        with self.assertRaises(ValidationException) as context:
            book = Book(
                title="Valid Title",
                author="Valid Author",
                year=0,  # Too little year
                status=BookStatus.AVAILABLE.value
            )
            book.validate()
        self.assertIn("Year must be between 1 and", str(context.exception))

    def test_missing_year(self):
        """
        Checks that a missing year causes a ValidationException.
        """
        with self.assertRaises(ValidationException) as context:
            book_data = {
                "id": "12345",
                "title": "Valid Title",
                "author": "Valid Author",
                "status": BookStatus.AVAILABLE.value
                # The year field is omitted
            }
            book = Book.from_json(book_data)
            book.validate()
        self.assertIn("Field 'year' must be of type int",
                      str(context.exception))

    def test_missing_status(self):
        """
        Checks that missing status causes a ValidationException.
        """
        with self.assertRaises(ValidationException) as context:
            book_data = {
                "id": "12345",
                "title": "Valid Title",
                "author": "Valid Author",
                "year": 2023  # The status field is omitted
            }
            book = Book.from_json(book_data)
            book.validate()
        self.assertIn("Fields cannot be empty: status", str(context.exception))


if __name__ == "__main__":
    unittest.main()
