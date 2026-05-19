from fastapi import FastAPI
from routers import users, articles, diversity, interactions, discovery

app = FastAPI(
    title="Pivot Divergent Content Delivery Network Engine",
    version="1.0.0"
)

# Bind all individual components directly onto the centralized app instance
app.include_router(users.router)
app.include_router(articles.router)
app.include_router(diversity.router)       # <-- The Diversity Engine Algorithmic Core
app.include_router(interactions.router)    # <-- Pure Engagement / Curation Tasks
app.include_router(discovery.router)
