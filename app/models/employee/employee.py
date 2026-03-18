from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50), unique=True, nullable=False)

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    full_name = Column(String(255), nullable=False)
    profile_image = Column(String(255), nullable=True)

    academic_degree = Column(String(100), nullable=True)
    academic_title = Column(String(100), nullable=True)
    position = Column(String(255), nullable=True)

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

    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    building = Column(String(100), nullable=True)
    floor = Column(String(20), nullable=True)
    room = Column(String(50), nullable=True)

    scopus_url = Column(Text, nullable=True)
    google_scholar_url = Column(Text, nullable=True)
    orcid_url = Column(Text, nullable=True)
    researchgate_url = Column(Text, nullable=True)
    academia_url = Column(Text, nullable=True)

    scientific_interests = Column(Text, nullable=True)
    publications = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=True)

    translations = relationship(
        "EmployeeTr",
        back_populates="employee",
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
