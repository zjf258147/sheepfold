from datetime import datetime

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.models.user import User


def write_audit_log(
    db: Session,
    user: User,
    action: str,
    module: str,
    resource_type: str,
    resource_id: str,
    resource_name: str,
    summary: str,
    change_reason: str | None = None,
    before_data: dict | None = None,
    after_data: dict | None = None,
    ip_address: str | None = None,
):
    db.add(AuditLog(
        operator_id=user.id,
        operator_name=f"{user.nickname or user.username}（{user.username}）",
        action=action,
        module=module,
        resource_type=resource_type,
        resource_id=resource_id,
        resource_name=resource_name,
        summary=summary,
        change_reason=change_reason,
        before_data=str(before_data) if before_data else None,
        after_data=str(after_data) if after_data else None,
        ip_address=ip_address,
        created_at=datetime.now(),
    ))