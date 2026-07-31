from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    func,
    String
)
from app.core.database import Base

class HeroCertificateTranslation(Base):
    __tablename__ = "hero_certificate_tr"

    id = Column(Integer, primary_key=True, index=True)
    certificate_id = Column(Integer, nullable=False)
    lang_code = Column(String(2), nullable=False)
    title = Column(Text, nullable=False)
    kicker = Column(String(255), nullable=True)
    signer = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
