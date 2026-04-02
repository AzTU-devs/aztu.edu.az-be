from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship


class DepartmentTr(Base):
    __tablename__ = "departments_tr"
    __table_args__ = (
        UniqueConstraint("department_code", "lang_code", name="uq_departments_tr_code_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    department_code = Column(
        String(50),
        ForeignKey("departments.department_code", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    department_name = Column(String(255), nullable=False)
    about_html = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    department = relationship("Department", back_populates="translations")
