from typing import Optional


VEICULO_NOT_FOUND_ERROR = "veiculo_not_found"


class BaseException(Exception):
    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        status_code: int = 400,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code


class NotFoundError(BaseException):
    pass
