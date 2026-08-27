from jsonschema import validate, ValidationError
from src.core.config import SCHEMA

class Schema:
    @staticmethod
    def validate_data(data: dict) -> bool:
        try:
            validate(instance=data, schema=SCHEMA)
            return True
        except ValidationError:
            return False

