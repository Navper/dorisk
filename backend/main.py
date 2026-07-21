import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from backend.config import validate_config
from backend.routers import auth, oauth, songs, history, admin

# Validar variables de entorno en el arranque
validate_config()

app = FastAPI(
    title="Dorisk API",
    description="Backend para la webapp colectiva musical Dorisk/MusicDrop",
    version="1.0.0"
)

# Configurar CORS para permitir peticiones desde el frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permitir cualquier origen para desarrollo
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
