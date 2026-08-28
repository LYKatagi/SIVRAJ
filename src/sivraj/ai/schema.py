
from jsonschema import ValidationError, validate

from sivraj.core.config import SCHEMA


class Schema:
    @staticmethod
    def validate_data(data) -> bool:
        try:
            validate(
                instance=data,
                schema=SCHEMA,
            )
            return True

        except ValidationError:
            return False

