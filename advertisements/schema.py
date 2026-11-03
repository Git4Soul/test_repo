from pydantic import BaseModel, ValidationError

from errors import HttpError


class CreateUser(BaseModel):
    name: str
    password: str


class UpdateUser(BaseModel):
    name: str | None = None
    password: str | None = None


def validate(json_data: dict, schema_cls: type[CreateUser | UpdateUser]) -> dict:
    try:
        return schema_cls(**json_data).model_dump()
    except ValidationError as err:
        errors = err.errors()
        for e in errors:
            e.pop("ctx", None)
        raise HttpError(errors, 400)
