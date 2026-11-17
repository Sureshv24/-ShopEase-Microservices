from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings
bearer = HTTPBearer(auto_error=False)
def current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)):
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(401, "Bearer token required", headers={"WWW-Authenticate":"Bearer"})
    try:
        claims = jwt.decode(credentials.credentials, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return {"user_id": int(claims["sub"]), "role": str(claims.get("role","")).lower()}
    except (JWTError, ValueError, KeyError, TypeError):
        raise HTTPException(401, "Invalid or expired token", headers={"WWW-Authenticate":"Bearer"})
def require_admin(user=Depends(current_user)):
    if user["role"] not in {"admin","administrator"}:
        raise HTTPException(403, "Administrator permission required")
    return user
