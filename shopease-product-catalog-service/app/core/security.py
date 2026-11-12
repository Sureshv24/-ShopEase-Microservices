from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings

bearer = HTTPBearer(auto_error=False)

def get_token_claims(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)):
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Bearer token required",
                            headers={"WWW-Authenticate": "Bearer"})
    try:
        claims = jwt.decode(credentials.credentials, settings.JWT_SECRET_KEY,
                            algorithms=[settings.JWT_ALGORITHM])
        if claims.get("sub") is None:
            raise ValueError("Missing subject")
        return claims
    except (JWTError, ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Invalid or expired token",
                            headers={"WWW-Authenticate": "Bearer"})

def current_user(claims=Depends(get_token_claims)):
    try:
        return {"user_id": int(claims["sub"]), "role": str(claims.get("role", "")).lower()}
    except (ValueError, TypeError, KeyError):
        raise HTTPException(status_code=401, detail="Invalid token claims")

def require_admin(user=Depends(current_user)):
    if user["role"] not in {"admin", "administrator"}:
        raise HTTPException(status_code=403, detail="Administrator permission required")
    return user