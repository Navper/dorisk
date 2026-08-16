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
    "http://localhost:8050",
    "http://127.0.0.1:8050",
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

# Programador de tareas en segundo plano (Lunes 02:00 AM España / 00:00 UTC)
import asyncio
from datetime import datetime, timezone

last_sweep_week = None

async def weekly_sweep_scheduler():
    global last_sweep_week
    while True:
        try:
            now = datetime.now(timezone.utc)
            current_week = now.strftime("%Y-W%W")
            # Lunes (weekday 0) a las 00:00 UTC (02:00 AM hora de España)
            if now.weekday() == 0 and now.hour == 0 and last_sweep_week != current_week:
                from backend.weekly_sweep import run_weekly_sweep
                print("⏰ [Scheduler] Ejecutando cierre semanal automático (Lunes 02:00 AM España)...")
                run_weekly_sweep()
                last_sweep_week = current_week
        except Exception as e:
            print(f"❌ Error en scheduler semanal: {e}")
            
        await asyncio.sleep(60)

@app.on_event("startup")
async def start_scheduler():
    asyncio.create_task(weekly_sweep_scheduler())

from fastapi.responses import FileResponse
import os

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@app.get("/")
async def root():
    index_path = os.path.join(root_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "status": "online",
        "app": "Dorisk",
        "description": "¡La canción del día está lista!"
    }

@app.get("/static/avatars/{filename}")
async def serve_avatar(filename: str):
    from backend.db_local import AVATARS_DIR
    file_path = os.path.join(AVATARS_DIR, filename)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Avatar no encontrado")

@app.get("/{filename:path}")
async def serve_static_files(filename: str):
    file_path = os.path.join(root_dir, filename)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Archivo no encontrado")


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
