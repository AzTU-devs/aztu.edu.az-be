from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship


class FacultyDirector(Base):
    __tablename__ = "faculty_directors"
    __table_args__ = (
        UniqueConstraint("faculty_code", name="uq_faculty_directors_code"),
    )

    id = Column(Integer, primary_key=True, index=True)
    faculty_code = Column(
        String(50),
        ForeignKey("faculties.faculty_code", ondelete="CASCADE"),
        nullable=False,
    )
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    father_name = Column(String(100))
    email = Column(String(255))
    phone = Column(String(50))
    room_number = Column(String(50))
    profile_image = Column(String(1024))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    faculty = relationship("Faculty", back_populates="director")
    translations = relationship(
        "FacultyDirectorTr",
        back_populates="director",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    working_hours = relationship(
        "FacultyDirectorWorkingHour",
        back_populates="director",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    scientific_events = relationship(
        "FacultyDirectorScientificEvent",
        back_populates="director",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    educations = relationship(
        "FacultyDirectorEducation",
        back_populates="director",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class FacultyDirectorTr(Base):
    __tablename__ = "faculty_director_tr"
    __table_args__ = (
        UniqueConstraint("director_id", "lang_code", name="uq_faculty_director_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    director_id = Column(
        Integer,
        ForeignKey("faculty_directors.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    scientific_degree = Column(String(255))
    scientific_title = Column(String(255))
    bio = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    director = relationship("FacultyDirector", back_populates="translations")
