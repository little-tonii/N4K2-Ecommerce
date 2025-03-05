from fastapi import FastAPI, HTTPException
from fastapi.concurrency import asynccontextmanager
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from .configs.exception_handler import global_exception_handler, http_exception_handler, validation_exception_handler
from .configs.database import client
from .routers import category_router, product_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if client:
        client.close()

app = FastAPI(title="Product Service", lifespan=lifespan)

origins = [
    "*"
]

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

app.include_router(category_router.router)
app.include_router(product_router.router)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)