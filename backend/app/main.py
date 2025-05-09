from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import users, analyses, chat, models

app = FastAPI(
    title="EVIverse API",
    description="API pour la plateforme de visualisation et d'analyse de modèles 3D",
    version="0.1.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # à sécuriser en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(users.router)
app.include_router(models.router)
app.include_router(analyses.router)
app.include_router(chat.router)

@app.get("/")
async def root():
    return {
        "message": "Bienvenue sur l'API EVIverse",
        "version": "0.1.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }
