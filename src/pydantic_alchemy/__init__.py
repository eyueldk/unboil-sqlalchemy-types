from typing import Any

from pydantic import TypeAdapter
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import JSON, Dialect, TypeDecorator


class PydanticJSONB(TypeDecorator):
    
    impl = JSONB
    cache_ok = True  # Performance hint
    __module__ = "sqlalchemy.dialects.postgresql" # for alembic

    def __init__(self, pydantic_type: type[Any]):
        super().__init__()
        self.pydantic_type = pydantic_type
        self.adapter = TypeAdapter(pydantic_type)

    def process_bind_param(self, value: Any, dialect: Dialect):
        if isinstance(value, self.pydantic_type):
            return self.adapter.dump_python(value)
        elif isinstance(value, dict):
            return value  # Already a dict, possibly from a deserialized source
        raise TypeError(f"Expected {self.pydantic_type} or dict, got {type(value)}")

    def process_result_value(self, value: Any, dialect: Dialect):
        if value is None:
            return None
        return self.adapter.validate_python(value)
        
    # for alembic
    def __repr__(self) -> str:
        return f"JSONB()"