import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from backend.config import validate_config, DEV_MODE
from backend.routers import auth, oauth, songs, history, admin

# Validar variables de entorno en el arranque
validate_config()

# Desactivar documentación Swagger/OpenAPI en producción
app = FastAPI(
    title="Dorisk API",
    description="Backend para la webapp colectiva musical Dorisk/MusicDrop",
    version="1.0.0",
    docs_url="/docs" if DEV_MODE else None,
    redoc_url="/redoc" if DEV_MODE else None,
    openapi_url="/openapi.json" if DEV_MODE else None,
)

# CORS restringido
allowed_origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://dorisk.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(auth.router)
app.include_router(oauth.router)
app.include_router(songs.router)
app.include_router(history.router)
app.include_router(admin.router)

@app.get("/")
async def root():
    return {
        "status": "online",
        "app": "Dorisk",
        "description": "¡La canción del día está lista!"
    }


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
