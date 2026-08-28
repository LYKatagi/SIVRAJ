from jsonschema import validate, ValidationError
from sivraj.core.config import SCHEMA

class Schema:
    @staticmethod
    def validate_data(data: dict) -> bool:
        
        validate(instance=data, schema=SCHEMA)
        return True
        

