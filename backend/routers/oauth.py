from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from backend.services import spotify_client, youtube_client

router = APIRouter(prefix="/api/auth", tags=["oauth"])

@router.get("/spotify")
async def authorize_spotify():
    """Redirige al usuario al portal de login de Spotify"""
    try:
        oauth = spotify_client.get_oauth_manager()
        auth_url = oauth.get_authorize_url()
        return RedirectResponse(auth_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al iniciar Spotify Auth: {e}")

@router.get("/spotify/callback")
async def spotify_callback(code: str):
    """Callback de Spotify que recibe el código de autorización"""
    try:
        oauth = spotify_client.get_oauth_manager()
        token_info = oauth.get_access_token(code, as_dict=True)
        if token_info:
            return HTMLResponse(content="""
                <html>
                    <body style="font-family: sans-serif; text-align: center; padding-top: 100px; background-color: #120820; color: #f5e8d8;">
                        <h1 style="color: #e8a0b4;">🎀 ¡Spotify Autorizado con éxito!</h1>
                        <p>Ya puedes cerrar esta pestaña y volver a Dorisk.</p>
                    </body>
                </html>
            """)
        raise Exception("No se pudo obtener el token de acceso.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en Spotify Callback: {e}")

@router.get("/youtube")
async def authorize_youtube():
    """Redirige al usuario al portal de login de Google (YouTube)"""
    try:
        flow = youtube_client.get_flow()
        authorization_url, state = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent"
        )
        return RedirectResponse(authorization_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al iniciar YouTube Auth: {e}")

@router.get("/youtube/callback")
async def youtube_callback(request: Request):
    """Callback de Google que recibe el código de autorización"""
    try:
        flow = youtube_client.get_flow()
        # Interceptar el query string de la petición
        flow.fetch_token(authorization_response=str(request.url))
        credentials = flow.credentials
        
        # Guardar las credenciales
        youtube_client.save_credentials(credentials)
        
        return HTMLResponse(content="""
            <html>
                <body style="font-family: sans-serif; text-align: center; padding-top: 100px; background-color: #120820; color: #f5e8d8;">
                    <h1 style="color: #e8a0b4;">▶ ¡YouTube Autorizado con éxito!</h1>
                    <p>Ya puedes cerrar esta pestaña y volver a Dorisk.</p>
                </body>
            </html>
        """)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en YouTube Callback: {e}")
