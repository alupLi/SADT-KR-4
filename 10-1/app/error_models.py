from pydantic import BaseModel
from datetime import datetime


class ErrorResponse(BaseModel):
    status_code: int
    error_type: str
    message: str
    timestamp: datetime
    path: str | None = None


class ValidationErrorResponse(ErrorResponse):
    error_type: str = "Validation Error"


class NotFoundErrorResponse(ErrorResponse):
    error_type: str = "Not Found"