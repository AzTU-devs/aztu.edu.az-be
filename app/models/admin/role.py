from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Text,
    DateTime,
    Table,
    ForeignKey,
    PrimaryKeyConstraint,
    Index,
)
from app.core.database import Base


role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False),
    Column("permission_id", Integer, ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False),
    Column("granted_at", DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)),
    PrimaryKeyConstraint("role_id", "permission_id", name="pk_role_permissions"),
    Index("ix_role_permissions_permission", "permission_id"),
)


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name_az = Column(String(100), nullable=False)
    name_en = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_system = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=True)


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False, index=True)
    domain = Column(String(50), nullable=False, index=True)
    action = Column(String(50), nullable=False)
    label_az = Column(String(200), nullable=False)
    label_en = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
