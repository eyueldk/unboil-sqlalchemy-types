
# Pydantic-Alchemy

A SQLAlchemy type decorator for storing and retrieving Pydantic models in PostgreSQL JSONB columns.
This library enables seamless integration between Pydantic and SQLAlchemy, allowing you to store validated data models directly in your database.

## Features
- Store Pydantic models in PostgreSQL JSONB columns
- Automatic validation and serialization/deserialization
- Works with Alembic migrations

## Installation
```bash
pip install pydantic-alchemy
```

## Usage Example
```python
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic_alchemy import PydanticJSONB


class Base(DeclarativeBase):
    pass

class Profile(BaseModel):
    age: int
    bio: str


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    profile: Mapped[Profile] = mapped_column(PydanticJSONB(Profile))

# Now, assigning a Profile instance to user.profile will automatically validate and serialize it.
```