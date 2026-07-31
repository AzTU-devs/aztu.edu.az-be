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
    # Who attested the certificate: 'qs' (ranking body) | 'aqas' (programme
    # accreditation agency). server_default keeps rows written before the
    # issuer migration — and any client that omits the field — on 'qs'.
    issuer = Column(String(16), nullable=False, server_default="qs", default="qs")
    # QS-only. AQAS certificates carry no rank position, hence nullable.
    rank_label = Column(Text, nullable=True)
    # QS-only ('world' | 'europe' | 'subject' | 'other'), hence nullable.
    family = Column(String(32), nullable=True)
    image = Column(Text, nullable=True)
    document = Column(Text, nullable=True)
    external_url = Column(Text, nullable=True)
    issued_date = Column(Date, nullable=True)
    display_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
