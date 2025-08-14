
# unboil-sqlalchemy-types


## Installation
```bash
pip install unboil-sqlalchemy-types
```

## Usage Example
```python
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from unboil_sqlalchemy_types import PydanticJSON


class Base(DeclarativeBase):
    pass

class Profile(BaseModel):
    age: int
    bio: str

Meta = str | int | dict

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    profile: Mapped[Profile] = mapped_column(PydanticJSON(Profile))
    meta: Mapped[Meta] = mapped_column(PydanticJSON(Meta))
```