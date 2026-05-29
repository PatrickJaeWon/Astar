import os
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def require_api_key(api_key: str = Security(_api_key_header)) -> str:
    expected = os.getenv("INTERNAL_API_KEY")
    if not expected:
        return "dev-no-key-configured"
    if api_key != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 API 키입니다.",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return api_key
