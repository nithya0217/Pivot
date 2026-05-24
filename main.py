from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from db import init_db, close_db
import interactions

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://pivot-frontend-1lehl2hvt-nithya-s-projects3.vercel.app",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interactions.router)

@app.get("/")
async def root():
    return {"message": "Pivot API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
