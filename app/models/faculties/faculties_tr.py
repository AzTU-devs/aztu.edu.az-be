from app.core.database import Base
from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint

class FacultyTr(Base):
    __tablename__ = "faculties_tr"
    __table_args__ = (
        UniqueConstraint("faculty_code", "lang_code", name="uq_faculties_tr_code_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    faculty_name = Column(String(255), nullable=False)
    faculty_code = Column(String(50), nullable=False)
    lang_code = Column(String(10), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)
