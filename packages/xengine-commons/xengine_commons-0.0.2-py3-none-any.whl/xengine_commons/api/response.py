from typing import Generic, TypeVar, Optional
from .status import APIStatus

T = TypeVar('T')


class Response(Generic[T]):
    def __init__(
        self,
        code: APIStatus,
        msg: str,
        data: Optional[T] = None
    ):
        self.code = code
        self.msg = msg
        self.data = data if data is not None else {}

    def to_dict(self) -> dict:
        """Convert the response to a dictionary"""
        return {
            "code": self.code.value,
            "msg": self.msg,
            "data": self.data
        }

    @classmethod
    def success(
        cls,
        msg: str = "Success",
        data: Optional[T] = None
    ) -> 'Response[T]':
        """Helper method for successful responses"""
        return cls(APIStatus.OK, msg, data)

    @classmethod
    def error(
        cls,
        code: APIStatus,
        msg: str,
        data: Optional[T] = None
    ) -> 'Response[T]':
        """Helper method for error responses"""
        return cls(code, msg, data)

    def __repr__(self) -> str:
        return f"Response(code={self.code}, msg={self.msg}, data={self.data})"

