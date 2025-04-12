from typing import Generic, TypeVar, cast

from ninja.errors import ValidationError
from pydantic import BaseModel

from unchained import Request
from unchained.dependencies.custom import BaseCustom

T = TypeVar("T")


class Header(BaseCustom, Generic[T]):
    def __init__(self, param_name: str | None = None, required: bool = True):
        super().__init__()
        self.param_name = param_name
        self.required = required
        self.annotation_type: type[T]

    def __call__(self, request: Request) -> T | None:
        headers = request.headers

        if self.param_name and self.param_name in headers:
            if issubclass(self.annotation_type, BaseModel):
                return cast(T, self.annotation_type.model_validate(headers))
            else:
                return self.annotation_type(headers[self.param_name])  # type: ignore

        if self.required:
            raise ValidationError([{"msg": f"Missing header: {self.param_name}"}])

        return None
