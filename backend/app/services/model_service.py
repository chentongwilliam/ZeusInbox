import os
import requests
import json
from datetime import datetime, timedelta

MODELS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models.json')
OPENROUTER_API = 'https://openrouter.ai/api/v1/models'
CACHE_EXPIRE_HOURS = 24

def fetch_models_from_openrouter():
    try:
        resp = requests.get(OPENROUTER_API)
        if resp.ok:
            data = resp.json()
            with open(MODELS_FILE, 'w', encoding='utf-8') as f:
                json.dump({
                    'models': data,
                    'last_update': datetime.utcnow().isoformat()
                }, f, ensure_ascii=False, indent=2)
            return data
        else:
            return []
    except Exception as e:
        print('Failed to fetch models:', e)
        return []

def get_models():
    if not os.path.exists(MODELS_FILE):
        return fetch_models_from_openrouter()
    try:
        with open(MODELS_FILE, 'r', encoding='utf-8') as f:
            cache = json.load(f)
            last_update = datetime.fromisoformat(cache.get('last_update', '1970-01-01T00:00:00'))
            if datetime.utcnow() - last_update > timedelta(hours=CACHE_EXPIRE_HOURS):
                return fetch_models_from_openrouter()
            return cache.get('models', [])
    except Exception as e:
        print('Failed to read models cache:', e)
        return fetch_models_from_openrouter() 