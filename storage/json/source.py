import json
import os
from typing import Dict, Generator, Any, List

from storage.json.exceptions import InvalidJsonFormatException
from storage.base.source import DataSource


class JsonSource(DataSource):
    """
    Implementation of DataStorage for working with JSON.

    This class provides functionality for loading and saving data in JSON format.
    It implements the `DataSource` interface and allows reading and writing dictionaries
    to a JSON file, ensuring the file exists and creating an empty one if it does not.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self._ensure_file_exists()

    def load(self) -> Generator[Dict, Any, None]:
        """
        Loads data from a JSON file as a generator.

        :return: A generator that yields data as dictionaries.
        :raises InvalidJsonFormatException: If the JSON file format is incorrect.
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                for obj_data in data:
                    yield obj_data
        except json.JSONDecodeError as e:
            raise InvalidJsonFormatException(f"Failed to parse JSON file: {e}")

    def save(self, data: List[Dict]) -> None:
        """
        Saves data to a JSON file.

        :param data: A list of dictionaries to save to the file.
        :return: None
        """
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )

    def _ensure_file_exists(self) -> None:
        """
        Ensures that the JSON file exists.
        If the file does not exist, it creates an empty file.

        :return: None
        """
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([], file)
