from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from config import settings

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_role(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)
):
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication credentials"
        )

    token = credentials.credentials
    role_map = {value: key for key, value in settings.api_tokens.items()}
    role = role_map.get(token)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return role


def require_role(required_roles: list[str]):
    def wrapper(role: str = Depends(get_current_role)):
        if role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden for this role"
            )
        return role

    return wrapper

