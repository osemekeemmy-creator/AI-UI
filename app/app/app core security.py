from fastapi import Security, HTTPException, Depends
from fastapi.security import APIKeyHeader
from config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(key: str = Security(api_key_header)):
    if key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return key
