from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    Date,
    func,
    Boolean,
    String
)
from app.core.database import Base

class HeroCertificate(Base):
    __tablename__ = "hero_certificate"

    id = Column(Integer, primary_key=True, index=True)
    certificate_id = Column(Integer, nullable=False, unique=True)
    rank_label = Column(Text, nullable=False)
    family = Column(String(32), nullable=False)
    image = Column(Text, nullable=True)
    document = Column(Text, nullable=True)
    external_url = Column(Text, nullable=True)
    issued_date = Column(Date, nullable=True)
    display_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
