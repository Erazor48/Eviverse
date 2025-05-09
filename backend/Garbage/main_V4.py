from backend.app.api import models_V2
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi
import os

from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from app.api import users, analyses, chat

# === Initialisation de l'app ===
app = FastAPI(
    title="EVIverse API",
    description="API pour la plateforme de visualisation et d'analyse de modèles 3D",
    version="0.1.0",
    docs_url=None,
    redoc_url=None
)

# Monter le dossier statique
static_path = os.path.join(os.path.dirname(__file__), "..", "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

# === Middleware CORS ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["openapi"] = "3.0.2"  # 👈 Forcer la version compatible
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# === Inclusion des routes ===
app.include_router(users.router)
app.include_router(models_V2.router)
app.include_router(analyses.router)
app.include_router(chat.router)

# === Swagger UI avec thème sombre dynamique ===
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(request: Request):
    swagger_ui = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="EVIverse API - Swagger UI",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui.css"
    )
    html = swagger_ui.body.decode("utf-8")
    
    # Injection CSS/JS pour le bouton dark mode
    injection = '''
    <link rel="stylesheet" type="text/css" href="/static/css/swagger-dark-mode.css">
    <script src="/static/js/swagger-dark-mode.js"></script>
    '''
    html = html.replace("</head>", f"{injection}</head>")
    
    return HTMLResponse(content=html, status_code=200)

# === ReDoc avec thème sombre dynamique ===
@app.get("/redoc", include_in_schema=False)
async def custom_redoc_html():
    redoc_html = get_redoc_html(
        openapi_url=app.openapi_url,
        title="EVIverse API - ReDoc",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    )
    html = redoc_html.body.decode("utf-8")
    
    injection = '''
    <link rel="stylesheet" type="text/css" href="/static/css/redoc-dark-mode.css">
    <script src="/static/js/redoc-dark-mode.js"></script>
    '''
    html = html.replace("</head>", f"{injection}</head>")
    
    return HTMLResponse(content=html, status_code=200)

# === Page d'accueil ===
@app.get("/")
async def root():
    return {
        "message": "Bienvenue sur l'API EVIverse",
        "version": "0.1.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }