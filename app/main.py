from fastapi import FastAPI
from app.routes import router

app = FastAPI()

# Include the routes from routes.py
app.include_router(router)