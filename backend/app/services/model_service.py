import os
import aiohttp
import json
import logging
from datetime import datetime, timedelta

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODELS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models.json')
OPENROUTER_API = 'https://openrouter.ai/api/v1/models'
CACHE_EXPIRE_HOURS = 24
REQUEST_TIMEOUT = 10  # 请求超时时间（秒）

async def fetch_models_from_openrouter():
    """异步获取模型列表"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(OPENROUTER_API, timeout=REQUEST_TIMEOUT) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    # 保存到缓存文件
                    cache_data = {
                        'models': data,
                        'last_update': datetime.utcnow().isoformat()
                    }
                    try:
                        with open(MODELS_FILE, 'w', encoding='utf-8') as f:
                            json.dump(cache_data, f, ensure_ascii=False, indent=2)
                        logger.info("Successfully cached models data")
                    except Exception as e:
                        logger.error(f"Failed to cache models: {str(e)}")
                    return data
                else:
                    logger.error(f"Failed to fetch models: HTTP {resp.status}")
                    return []
    except asyncio.TimeoutError:
        logger.error("Timeout while fetching models from OpenRouter")
        return []
    except Exception as e:
        logger.error(f"Error fetching models: {str(e)}")
        return []

def get_models():
    """获取模型列表，优先使用缓存"""
    if not os.path.exists(MODELS_FILE):
        logger.info("No cache file found, will fetch from OpenRouter")
        return []
        
    try:
        with open(MODELS_FILE, 'r', encoding='utf-8') as f:
            cache = json.load(f)
            last_update = datetime.fromisoformat(cache.get('last_update', '1970-01-01T00:00:00'))
            
            # 检查缓存是否过期
            if datetime.utcnow() - last_update > timedelta(hours=CACHE_EXPIRE_HOURS):
                logger.info("Cache expired, will fetch from OpenRouter")
                return []
                
            logger.info("Using cached models data")
            return cache.get('models', [])
    except Exception as e:
        logger.error(f"Failed to read models cache: {str(e)}")
        return [] 