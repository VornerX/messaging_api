from fastapi import FastAPI

from messaging_api.routes import app_routes

app = FastAPI(routes=app_routes)
