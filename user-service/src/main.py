
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from .configs.exception_handler import global_exception_handler, http_exception_handler, validation_exception_handler
from pydantic import ValidationError
from .configs.database import engine, init_db
from fastapi.middleware.cors import CORSMiddleware
from .routers import user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_db()
        yield
    finally:
        await engine.dispose()

app = FastAPI(lifespan=lifespan, title="User Service")

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

app.include_router(user_router.router)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)