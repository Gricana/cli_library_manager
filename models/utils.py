import uuid


def generate_unique_id() -> str:
    """
    Generates a unique identifier.

    :return: A string representing a unique identifier.
    """
    return str(uuid.uuid4())
