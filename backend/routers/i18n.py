from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()

LANGUAGES = {
    "en": {
        "welcome": "Welcome to SoulFetch!",
        "sync": "Sync Now",
        "user": "User Management",
        "codegen": "Code Generation",
        "accessibility": "Accessibility",
        "visualization": "Visualization"
    },
    "es": {
        "welcome": "¡Bienvenido a SoulFetch!",
        "sync": "Sincronizar",
        "user": "Gestión de Usuarios",
        "codegen": "Generación de Código",
        "accessibility": "Accesibilidad",
        "visualization": "Visualización"
    }
}

@router.get("/i18n/{lang}")
def get_translations(lang: str):
    try:
        translations = LANGUAGES.get(lang, LANGUAGES["en"])
        return JSONResponse(content=translations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
