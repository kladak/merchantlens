"""MerchantLens FastAPI entrypoint — synthetic product analytics demo."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.data import get_store
from app.routers import bundles, cohorts, health, products


@asynccontextmanager
async def lifespan(_app: FastAPI):
    get_store()  # warm seed on startup
    yield


app = FastAPI(
    title="MerchantLens",
    description=(
        "Educational product analytics demo with bundle lift scoring. "
        "Synthetic commerce data only — not affiliated with any prior employer."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(bundles.router)
app.include_router(cohorts.router)
app.include_router(products.router)
