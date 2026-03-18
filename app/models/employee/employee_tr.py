from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship


class EmployeeTr(Base):
    __tablename__ = "employee_tr"
    __table_args__ = (
        UniqueConstraint("employee_code", "lang_code", name="uq_employee_tr_code_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(
        String(50),
        ForeignKey("employees.employee_code", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    biography = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=True)

    employee = relationship("Employee", back_populates="translations")
