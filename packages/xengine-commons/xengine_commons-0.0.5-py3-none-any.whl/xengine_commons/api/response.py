from typing import Optional
from .status import APIStatus
from utype import Schema


class ResponseSchema(Schema):
    code: APIStatus
    msg: Optional[str]
    data: Schema | dict

    def __init__(
        self,
        code: APIStatus,
        msg: Optional[str] = None,
        data: Schema | dict = None,
    ):
        super().__init__(code=code, msg=msg or code.description, data=data or {})

    @classmethod
    def success(
        cls, msg: Optional[str] = None, data: Schema | dict = None
    ) -> "ResponseSchema":
        """Helper method for successful responses"""
        return cls(APIStatus.OK, msg, data)

    @classmethod
    def error(
        cls,
        code: APIStatus,
        msg: Optional[str] = None,
        data: Schema | dict = None,
    ) -> "ResponseSchema":
        """Helper method for error responses"""
        print(data)
        return cls(code, msg, data)

    def __repr__(self) -> str:
        return f"Response(code={self.code}, msg={self.msg}, data={self.data})"

