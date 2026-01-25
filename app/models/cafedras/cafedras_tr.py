from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

class CafedraTr(Base):
    __tablename__ = "cafedras_tr"
    __table_args__ = (
        UniqueConstraint("cafedra_code", "lang_code", name="uq_cafedras_tr_code_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    cafedra_name = Column(String(255), nullable=False)
    cafedra_code = Column(
        String(50),
        ForeignKey("cafedras.cafedra_code", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)

    cafedra = relationship("Cafedra", back_populates="translations")
