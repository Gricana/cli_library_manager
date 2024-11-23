from abc import ABC, abstractmethod
from typing import Any, Dict, Generator


class DataSource(ABC):
    """
    Interface for managing data sources.

    This interface defines methods for loading and saving data,
    enabling interaction with different types of storage (e.g., JSON, DB, etc.).
    """

    @abstractmethod
    def load(self) -> Generator[Dict, Any, None]:
        """
        Loads data from the source.

        This method should be implemented to read data from a specific source
        and yield it as dictionaries.

        :return: A generator yielding data items as dictionaries.
        """
        pass

    @abstractmethod
    def save(self, data: list[Dict]) -> None:
        """
        Saves data to the source.

        This method should be implemented to write data to a specific source.

        :param data: A list of dictionaries representing the data to save.
        """
        pass
