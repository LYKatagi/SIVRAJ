from jsonschema import ValidationError, validate

from sivraj.core.config import SCHEMA
from sivraj.log.logger import get_logger


class Schema:
    @staticmethod
    def validate_data(data) -> bool:
        try:
            logger = get_logger(__name__)
            validate(
                instance=data,
                schema=SCHEMA,
            )

            return True

        except ValidationError:
            return False
