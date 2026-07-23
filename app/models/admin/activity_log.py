from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Index,
)
from sqlalchemy.dialects.postgresql import JSONB

from app.core.database import Base


class AdminActivityLog(Base):
    """One row per audited mutation.

    Only the rendered-at-read-time message is human facing; nothing in this table
    is translated or formatted, so wording can change with no backfill.

    ``admin_user_id`` is nullable and ``ON DELETE SET NULL``: a failed login has no
    actor, and deleting an admin must never erase their history. ``admin_username``
    is therefore stored denormalised and is the only actor field guaranteed present.
    """

    __tablename__ = "admin_activity_log"

    id = Column(BigInteger, primary_key=True)
    admin_user_id = Column(
        Integer, ForeignKey("admin_users.id", ondelete="SET NULL"), nullable=True
    )
    admin_username = Column(String(255), nullable=False)

    action_key = Column(String(100), nullable=False)
    domain = Column(String(50), nullable=False)

    method = Column(String(10), nullable=False)
    path = Column(Text, nullable=False)
    route_template = Column(Text, nullable=True)

    target_type = Column(String(50), nullable=True)
    target_id = Column(Text, nullable=True)
    target_label = Column(Text, nullable=True)

    status_code = Column(Integer, nullable=False)
    outcome = Column(String(20), nullable=False, default="success")

    ip = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    request_id = Column(String(36), nullable=True)
    # What was sent and what came back, both sanitised and size-capped before
    # they reach this table — see app/core/audit_payload.py.
    request_body = Column(JSONB, nullable=True)
    response_body = Column(JSONB, nullable=True)
    meta = Column(JSONB, nullable=True)

    created_at = Column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    # Names mirror migrations_all_models.sql exactly — that file, not this model,
    # is the schema of record.
    __table_args__ = (
        Index("ix_activity_created_at", created_at.desc()),
        Index("ix_activity_admin_created", admin_user_id, created_at.desc()),
        Index("ix_activity_action", action_key),
        Index("ix_activity_domain", domain),
        Index("ix_activity_target", target_type, target_id),
    )
