from fastapi.routing import APIRouter

from backend.web.api import images, monitoring, chat, security, echoes

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(security.router, prefix="/auth", tags=["auth"])
api_router.include_router(images.router, prefix="/images", tags=["images"])
api_router.include_router(chat.router, prefix="/bot", tags=["bot"])
api_router.include_router(echoes.router, prefix="/echoes", tags=["echoes"])
