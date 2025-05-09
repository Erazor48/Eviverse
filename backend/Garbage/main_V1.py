from backend.app.api import models_V2
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.api import users, analyses, chat

app = FastAPI(
    title="EVIverse API",
    description="API pour la plateforme de visualisation et d'analyse de modèles 3D",
    version="0.1.0",
    swagger_ui_parameters={
        "syntaxHighlight.theme": "monokai"  # Thème sombre pour la syntaxe
    }
)

# Monter le dossier statique
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En développement, à restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(users.router)
app.include_router(models_V2.router)
app.include_router(analyses.router)
app.include_router(chat.router)

# Routes personnalisées pour les docs avec thème sombre
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(request: Request):
    from fastapi.openapi.docs import get_swagger_ui_html
    
    swagger_ui = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui.css",
    )
    
    # Injecter notre script pour le basculement du thème
    html_content = swagger_ui.body.decode("utf-8")
    
    # Ajouter CSS et JS pour le thème sombre
    html_content = html_content.replace(
        "</head>",
        '<link rel="stylesheet" href="/static/swagger-ui-dark.css" id="dark-theme-css">\n'
        '<script src="/static/theme-toggle.js" defer></script>\n'
        '</head>'
    )
    
    return HTMLResponse(html_content)

@app.get("/redoc", include_in_schema=False)
async def custom_redoc_html():
    from fastapi.openapi.docs import get_redoc_html
    
    redoc_html = get_redoc_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - ReDoc",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
    )
    
    # Injecter notre script pour le basculement du thème
    html_content = redoc_html.body.decode("utf-8")
    html_content = html_content.replace(
        "</head>",
        '<link rel="stylesheet" href="/static/dark-theme.css" id="dark-theme-css">\n'
        '<script src="/static/theme-toggle.js" defer></script>\n'
        '</head>'
    )
    
    return HTMLResponse(html_content)

@app.get("/")
async def root():
    return {
        "message": "Bienvenue sur l'API EVIverse",
        "version": "0.1.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }