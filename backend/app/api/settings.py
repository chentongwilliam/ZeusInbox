from fastapi import APIRouter, HTTPException
from app.utils.env_manager import update_language_setting, get_language_setting, read_env

router = APIRouter()

@router.post("/language/save")
async def save_language_setting(data: dict):
    """Save language setting to .env file"""
    try:
        language = data.get('language', 'en')
        update_language_setting(language)
        return {"status": "success", "message": "Language updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/language/get")
async def get_language():
    """Get language setting from .env file"""
    try:
        language = get_language_setting()
        return {"language": language}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all")
async def get_all_settings():
    """Get all settings from .env file"""
    try:
        env_vars = read_env()
        return {
            "language": env_vars.get("LANGUAGE", "en"),
            "email_update_interval": int(env_vars.get("EMAIL_UPDATE_INTERVAL", 5))
            # 后续可继续添加
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 