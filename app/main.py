from fastapi import FastAPI

from app.database import Base, engine, get_db
from app import models
from app.routers import analytics, auth_routes, expenses

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SpendWise API",
    description="Track expenses securely with user accounts.",
    version="5.0.0",
)


@app.get("/")
def home():
    return {
        "message": "Welcome to SpendWise API",
        "docs": "/docs",
    }


app.include_router(auth_routes.router)
app.include_router(expenses.router)
app.include_router(analytics.router)
