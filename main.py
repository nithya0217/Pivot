from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import init_db, close_db

# Import the router objects directly from your flat files
from users import router as users_router
from articles import router as articles_router
from diversity import router as diversity_router
from interactions import router as interactions_router
from discovery import router as discovery_router

app = FastAPI(
    title="Pivot Divergent Content Delivery Network Engine",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Bind the individual components directly onto the app instance
app.include_router(users_router)
app.include_router(articles_router)
app.include_router(diversity_router)
app.include_router(interactions_router)
app.include_router(discovery_router)

@app.on_event("startup")
async def startup():
    """Initialize database connection on app startup"""
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    """Close database connection on app shutdown"""
    await close_db()

@app.get("/", tags=["Root Gateway Entry"])
async def root_gateway_index():
    return {
        "status": "online",
        "documentation_path": "/docs"
    }


