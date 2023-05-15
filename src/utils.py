from src.database import SessionLocal
from typing import Generic, TypeVar, Union
from pydantic.generics import GenericModel


T = TypeVar("T")


class GenericResponse(GenericModel, Generic[T]):
    code: str
    message: str
    value: Union[T, None]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
