from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class FacultyDeputyDean(Base):
    __tablename__ = "faculty_deputy_deans"

    id = Column(Integer, primary_key=True, index=True)
    faculty_code = Column(
        String(50),
        ForeignKey("faculties.faculty_code", ondelete="CASCADE"),
        nullable=False,
    )
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    father_name = Column(String(100))
    scientific_name = Column(String(255))
    scientific_degree = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    duty = Column(String(255))
    profile_image = Column(String(1024))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    faculty = relationship("Faculty", back_populates="deputy_deans")


class FacultyCouncilMember(Base):
    __tablename__ = "faculty_scientific_council"

    id = Column(Integer, primary_key=True, index=True)
    faculty_code = Column(
        String(50),
        ForeignKey("faculties.faculty_code", ondelete="CASCADE"),
        nullable=False,
    )
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    father_name = Column(String(100))
    duty = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    faculty = relationship("Faculty", back_populates="scientific_council")


class FacultyWorker(Base):
    __tablename__ = "faculty_workers"

    id = Column(Integer, primary_key=True, index=True)
    faculty_code = Column(
        String(50),
        ForeignKey("faculties.faculty_code", ondelete="CASCADE"),
        nullable=False,
    )
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    father_name = Column(String(100))
    duty = Column(String(255), nullable=False)
    scientific_name = Column(String(255))
    scientific_degree = Column(String(255))
    email = Column(String(255))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    faculty = relationship("Faculty", back_populates="workers")
