from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.database import get_db
from app.models.enums import UserRole
from app.models.user import User

bearer_scheme = HTTPBearer(auto_error=True)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token 无效或已过期",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: int | None = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload 缺少 user_id",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.status != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已被禁用，请联系管理员",
        )

    return user


def require_roles(*roles: str):
    """仅允许指定角色访问。ADMIN 拥有全部权限。"""

    async def checker(user: User = Depends(get_current_user)) -> User:
        if user.role == UserRole.ADMIN.value:
            return user
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足，请联系管理员",
            )
        return user

    return checker


def get_current_admin(user: User = Depends(get_current_user)) -> User:
    """仅管理员可访问。"""
    if user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限",
        )
    return user


# 预定义角色权限组
AllowWarehouseOrAbove = require_roles(UserRole.ADMIN.value, UserRole.WAREHOUSE.value)
AllowQualityOrAbove = require_roles(UserRole.ADMIN.value, UserRole.QUALITY.value)
AllowProductionOrAbove = require_roles(UserRole.ADMIN.value, UserRole.PRODUCTION.value)
AllowAllRoles = require_roles(
    UserRole.ADMIN.value, UserRole.WAREHOUSE.value, UserRole.QUALITY.value,
    UserRole.PRODUCTION.value, UserRole.TEST_ENGINEER.value, UserRole.STAFF.value,
)