from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.model_service import fetch_models_from_openrouter
import logging
import asyncio

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ZeusInbox API",
    description="Backend API for ZeusInbox email assistant",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to ZeusInbox API"}

# Import and include routers
from app.api import email, model, settings
app.include_router(email.router, prefix="/api/email", tags=["email"])
app.include_router(model.router, prefix="/api", tags=["model"])
app.include_router(settings.router, prefix="/api/settings", tags=["settings"])

@app.on_event("startup")
async def startup_event():
    """在应用启动时异步加载模型"""
    logger.info("Starting to fetch models from OpenRouter...")
    try:
        # 设置超时时间
        async with asyncio.timeout(30):  # 30秒超时
            await fetch_models_from_openrouter()
        logger.info("Successfully fetched models from OpenRouter")
    except asyncio.TimeoutError:
        logger.error("Timeout while fetching models from OpenRouter")
    except Exception as e:
        logger.error(f"Error fetching models from OpenRouter: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting uvicorn server...")
    uvicorn.run(app, host="0.0.0.0", port=8001) 