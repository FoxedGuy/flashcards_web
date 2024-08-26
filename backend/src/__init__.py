from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import database as models

from .config import Settings
from .user.router import router as user_router

import logging as l

sett = Settings()

l.getLogger().setLevel(l.INFO)
l.log(l.ERROR, sett.root_path)
app = FastAPI(root_path=sett.root_path,
              title="Flashcards",
              description="Flashcards is a simple application for learning",
              version="0.0.1-dev",
              swagger_ui_parameters={"docExpansion": "none"},
              # docs_url=f"{sett.root_path}/docs",
              # redoc_url=f"{sett.root_path}/redoc",
              # openapi_prefix=sett.root_path,
              # openapi_url=f"/openapi.json",
              )
# app.mount("/ws", socket_app)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
