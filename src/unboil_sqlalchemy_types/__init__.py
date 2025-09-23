from typing import Any
from pydantic import ConfigDict, SecretStr
from pydantic_core import PydanticSerializationError
from sqlalchemy import Dialect, TypeDecorator, JSON

__all__ = [
    "PydanticJSON"
]

def serialize(obj: Any) -> Any:
    if isinstance(obj, SecretStr):
        return obj.get_secret_value()
    elif isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize(v) for v in obj]
    return obj

class PydanticJSON(TypeDecorator):
    
    impl = JSON
    cache_ok = True  # Performance hint
    __module__ = "sa" # for alembic to do sa.JSON()

    def __init__(self, pydantic_type: type[Any]):
        from pydantic import TypeAdapter
        super().__init__()
        self.pydantic_type = pydantic_type
        self.adapter = TypeAdapter(pydantic_type)

    def process_bind_param(self, value: Any, dialect: Dialect):
        if isinstance(value, dict):
            return serialize(value)  # Already a dict, possibly from a deserialized source
        else:
            dump = self.adapter.dump_python(value)
            return serialize(dump)

    def process_result_value(self, value: Any, dialect: Dialect):
        if value is None:
            return None
        return self.adapter.validate_python(value)
        
    # for alembic
    def __repr__(self) -> str:
        return f"JSON()"