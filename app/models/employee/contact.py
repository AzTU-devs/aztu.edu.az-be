from app.core.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship


class Contact(Base):
    __tablename__ = "employee_contacts"
    __table_args__ = (
        UniqueConstraint("employee_code", name="uq_employee_contacts_code"),
    )

    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(
        String(50),
        ForeignKey("employees.employee_code", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    email = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    building = Column(String(100), nullable=False)
    floor = Column(String(20), nullable=False)
    room = Column(String(50), nullable=False)

    employee = relationship("Employee", back_populates="contact")
