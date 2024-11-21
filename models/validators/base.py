from dataclasses import fields
from typing import Dict, Type

from models.exceptions import ValidationException


class Validator:
    """
    Class for validating model data.

    This class is used to check the model data to make sure
    that they match the expected types, required fields,
    and do not contain empty values.
    """

    def __init__(self, model_class: Type):
        """
        Initializes a validator for the specified model class.

        :param model_class: The class of the model whose data will be validated.
        """
        self.model_class = model_class

    def validate_data(self, data: Dict) -> None:
        """
        Checks data for compliance with all validation rules.

        :param data: Model data in the form of a dictionary,
                     where the keys are the names of the fields,
                     and the values are the corresponding values.
        :raises ValidationException: If the data is not validated.
        """
        errors = []
        errors.extend(self._check_required_fields(data))
        errors.extend(self._check_data_types(data))
        errors.extend(self._check_empty_fields(data))

        if errors:
            raise ValidationException("; ".join(errors))

    def _check_required_fields(self, data: Dict) -> list:
        """
        Checks that all required fields are present in the data.

        :param data: Model data.
        :return: List of errors if any required fields are missing.
        """
        required_fields = [f.name for f in fields(self.model_class) if
                           f.init and f.default is f.default_factory]
        missing_fields = [f for f in required_fields if f not in data]

        if missing_fields:
            return [f"Missing required fields: {', '.join(missing_fields)}"]
        return []

    def _check_data_types(self, data: Dict) -> list:
        """
        Verifies that the data matches the expected types for each field.

        :param data: Model data.
        :return: List of errors if the data type is not as expected.
        """
        errors = []
        for field_info in fields(self.model_class):
            field_name = field_info.name
            if field_name in data:
                expected_type = field_info.type
                if not isinstance(data[field_name], expected_type):
                    errors.append(
                        f"Field '{field_name}' must be of "
                        f"type {expected_type.__name__}")
        return errors

    def _check_empty_fields(self, data: Dict) -> list:
        """
        Проверяет, что строковые поля не пустые.

        :param data: Данные модели.
        :return: Список ошибок, если строковые поля пусты.
        """
        errors = []
        string_fields = [f.name for f in fields(self.model_class)
                         if f.type is str]
        empty_fields = [field for field in string_fields
                        if not data.get(field, "").strip()]
        if empty_fields:
            errors.append(f"Fields cannot be empty: {', '.join(empty_fields)}")
        return errors
