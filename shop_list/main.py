from fastapi import FastAPI
from shop_list.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
    )

    @app.get("/health-check")
    async def health_check():
        return {'status': 'ok'}

    return app
