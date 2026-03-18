from app.core.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship


class EducationTr(Base):
    __tablename__ = "education_tr"
    __table_args__ = (
        UniqueConstraint("education_id", "lang_code", name="uq_education_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    education_id = Column(
        Integer,
        ForeignKey("education.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    institution = Column(String(255), nullable=True)
    specialization = Column(String(255), nullable=True)

    education = relationship("Education", back_populates="translations")
