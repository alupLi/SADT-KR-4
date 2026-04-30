from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime

from app.exceptions import CustomExceptionA, CustomExceptionB
from app.error_models import ValidationErrorResponse, NotFoundErrorResponse
from app.routers import items

app = FastAPI(
    title="Custom Exceptions Demo",
    description="Демонстрация пользовательской обработки ошибок",
    version="1.0.0"
)

app.include_router(items.router)

@app.exception_handler(CustomExceptionA)
async def custom_exception_a_handler(request: Request, exc: CustomExceptionA):
    return JSONResponse(
        status_code=exc.status_code,
        content=ValidationErrorResponse(
            status_code=exc.status_code,
            error_type="Validation Error",
            message=exc.message,
            timestamp=datetime.now(),
            path=request.url.path
        ).model_dump()
    )

@app.exception_handler(CustomExceptionB)
async def custom_exception_b_handler(request: Request, exc: CustomExceptionB):
    return JSONResponse(
        status_code=exc.status_code,
        content=NotFoundErrorResponse(
            status_code=exc.status_code,
            error_type="Not Found",
            message=exc.message,
            timestamp=datetime.now(),
            path=request.url.path
        ).model_dump()
    )

@app.get("/")
def root():
    return {"message": "API с пользовательской обработкой ошибок"}

@app.get("/health")
def health():
    return {"status": "ok"}