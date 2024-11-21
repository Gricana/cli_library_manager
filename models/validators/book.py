from datetime import datetime
from typing import Dict

from models.constants import BookStatus
from models.exceptions import ValidationException
from models.validators.base import Validator


class BookValidator(Validator):
    """
    Validator for the book model.

    This validator extends the base validator
    and adds checks for the status field and year of publication.
    """

    def __init__(self):
        """
        Initializes the validator for the `Book` model.
        """
        from models.book import Book

        super().__init__(Book)

    def validate_data(self, data: Dict) -> None:
        """
        Checks book data for compliance with validation rules.

        :param data: Book data in the form of a dictionary.
        :raises ValidationException: If the data is not validated.
        """
        super().validate_data(data)
        errors = []
        errors.extend(self._check_status(data))
        errors.extend(self._check_year(data))

        if errors:
            raise ValidationException("; ".join(errors))

    def _check_status(self, data: Dict) -> list:
        """
        Checks that the Book status is a valid value.

        :param data: Book data.
        :return: List of errors if the book status is invalid.
        """
        if data.get("status") not in [status.value for status in BookStatus]:
            return [f"Incorrect status: {data.get('status')}. "
                    f"Valid values: {[s.value for s in BookStatus]}"]
        return []

    def _check_year(self, data: Dict) -> list:
        """
        Checks that the book's publication year is within an acceptable range.

        :param data: Book data.
        :return: List of errors if the year of publication is incorrect.
        """
        year = data.get('year')
        if year is None:
            return ["Year is required."]

        current_year = datetime.now().year

        if not (1 <= year <= current_year):
            return [f"Year must be between 1 and {current_year}."]
        return []
