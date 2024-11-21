from enum import Enum


class BookStatus(Enum):
    """
    An enumeration representing the possible book statuses.

    Statuses:
    - AVAILABLE: the book is available for issue.
    - ISSUED: the book has been issued.
    """
    AVAILABLE = "в наличии"
    ISSUED = "выдана"

    @staticmethod
    def get_status_choices():
        """
        Returns a list of all possible status values.

        :return: List of strings with possible statuses.
        """
        return [status.value for status in BookStatus]
