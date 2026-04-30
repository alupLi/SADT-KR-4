from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from datetime import datetime


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error['loc'])
        message = error['msg']
        errors.append({
            "field": field,
            "message": message,
            "type": error['type']
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status_code": 422,
            "error_type": "Validation Error",
            "message": "Ошибка валидации входных данных",
            "details": errors,
            "timestamp": datetime.now().isoformat(),
            "path": request.url.path
        }
    )


async def generic_validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status_code": 422,
            "error_type": "Pydantic Validation Error",
            "message": str(exc),
            "timestamp": datetime.now().isoformat(),
            "path": request.url.path
        }
    )