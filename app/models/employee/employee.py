from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50), unique=True, nullable=False)
    profile_image = Column(String(255), nullable=True)

    faculty_code = Column(
        String(50),
        ForeignKey("faculties.faculty_code", ondelete="SET NULL"),
        nullable=True,
    )
    cafedra_code = Column(
        String(50),
        ForeignKey("cafedras.cafedra_code", ondelete="SET NULL"),
        nullable=True,
    )

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=True)

    translations = relationship(
        "EmployeeTr",
        back_populates="employee",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    contact = relationship(
        "Contact",
        back_populates="employee",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    research = relationship(
        "Research",
        back_populates="employee",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    office_hours = relationship(
        "OfficeHour",
        back_populates="employee",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    educations = relationship(
        "Education",
        back_populates="employee",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    courses = relationship(
        "TeachingCourse",
        back_populates="employee",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
