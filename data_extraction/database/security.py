
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import settings

bearer_scheme = HTTPBearer(auto_error=False)

def verify_jwt(token: str) -> bool:
    """
    Actual JWT verification logic belongs here.
    For demonstration, we do a dummy check:
    If token == settings.jwt_secret -> valid.
    In real code:
      - decode token using pyjwt
      - check signature, expiry, issuer, etc.
    """
    # following implementation will for future use
    # try:
    #     payload = jwt.decode(
    #         token,
    #         settings.jwt_secret,
    #         algorithms=["HS256"]  # or whichever your issuer uses
    #     )
    #     # Optionally check 'exp', 'iss', 'sub', etc.
    #     return True
    # except PyJWTError:
    #     return False
    return token == settings.jwt_secret


async def require_jwt(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    """
    If auth is enabled, require a valid Bearer token.
    If auth is disabled, do nothing.
    """
    # 1. If auth is disabled, skip checks
    if not settings.auth_enabled:
        return  # let request pass

    # 2. If no credentials provided, raise 403
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authentication is required but no credentials provided."
        )

    # 3. Validate token
    token = credentials.credentials
    if not verify_jwt(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    # If valid, do nothing (just let request pass)
