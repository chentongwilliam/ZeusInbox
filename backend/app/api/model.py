from fastapi import APIRouter
from app.services.model_service import get_models

router = APIRouter()

@router.get('/models')
def list_models():
    """获取OpenRouter模型列表（自动缓存和更新）"""
    return get_models() 