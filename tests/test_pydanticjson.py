import pytest
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import registry, mapped_column, Mapped, Session
from pydantic import BaseModel
from unboil_sqlalchemy_types import PydanticJSON


mapper_registry = registry()
Base = mapper_registry.generate_base()


class Example(BaseModel):
    x: int
    y: str

class ExampleTable(Base):
    __tablename__ = "example_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[Example] = mapped_column(PydanticJSON(Example))

def test_pydanticjson_basemodel():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        obj = Example(x=1, y="foo")
        row = ExampleTable(data=obj)
        session.add(row)
        session.commit()
        loaded = session.query(ExampleTable).first()
        assert loaded is not None
        assert isinstance(loaded.data, Example)
        assert loaded.data.x == 1
        assert loaded.data.y == "foo"


import typing
from pydantic import SecretStr

class ExampleSecret(BaseModel):
    x: int
    secret: SecretStr

class ExampleSecretTable(Base):
    __tablename__ = "example_secret_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[ExampleSecret] = mapped_column(PydanticJSON(ExampleSecret))

def test_pydanticjson_secretstr():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        obj = ExampleSecret(x=42, secret=SecretStr("topsecret"))
        row = ExampleSecretTable(data=obj)
        session.add(row)
        session.commit()
        loaded = session.query(ExampleSecretTable).first()
        assert loaded is not None
        assert isinstance(loaded.data, ExampleSecret)
        assert loaded.data.x == 42
        assert loaded.data.secret.get_secret_value() == "topsecret"


from pydantic import TypeAdapter

class ExampleA(BaseModel):
    a: int

class ExampleB(BaseModel):
    b: str

ExampleUnion = typing.Union[str, int, ExampleA, ExampleB]

class ExampleUnionTable(Base):
    __tablename__ = "example_union_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[object] = mapped_column(PydanticJSON(ExampleUnion))

def test_pydanticjson_union():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        obj_a = ExampleA(a=123)
        obj_b = ExampleB(b="bar")
        obj_str = "hello"
        obj_int = 42
        row_a = ExampleUnionTable(data=obj_a)
        row_b = ExampleUnionTable(data=obj_b)
        row_str = ExampleUnionTable(data=obj_str)
        row_int = ExampleUnionTable(data=obj_int)
        session.add_all([row_a, row_b, row_str, row_int])
        session.commit()
        loaded = session.query(ExampleUnionTable).order_by(ExampleUnionTable.id).all()
        assert len(loaded) == 4
        assert isinstance(loaded[0].data, ExampleA)
        assert loaded[0].data.a == 123
        assert isinstance(loaded[1].data, ExampleB)
        assert loaded[1].data.b == "bar"
        assert loaded[2].data == "hello"
        assert loaded[3].data == 42
