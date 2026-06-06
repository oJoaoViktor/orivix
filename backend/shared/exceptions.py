from dataclasses import dataclass, field
from typing import Any


@dataclass
class AppError:
    code: str
    message: str
    details: dict = field(default_factory=dict)


@dataclass
class Result:
    success: bool
    data: Any = None
    error: AppError | None = None

    @classmethod
    def ok(cls, data=None) -> "Result":
        return cls(success=True, data=data)

    @classmethod
    def fail(cls, code: str, message: str, details: dict | None = None) -> "Result":
        return cls(success=False, error=AppError(code=code, message=message, details=details or {}))
