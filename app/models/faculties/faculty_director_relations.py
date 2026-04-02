from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship


class FacultyDirectorWorkingHour(Base):
    __tablename__ = "faculty_director_working_hours"

    id = Column(Integer, primary_key=True, index=True)
    director_id = Column(
        Integer,
        ForeignKey("faculty_directors.id", ondelete="CASCADE"),
        nullable=False,
    )
    time_range = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    director = relationship("FacultyDirector", back_populates="working_hours")
    translations = relationship(
        "FacultyDirectorWorkingHourTr",
        back_populates="working_hour",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class FacultyDirectorWorkingHourTr(Base):
    __tablename__ = "faculty_director_working_hour_tr"
    __table_args__ = (
        UniqueConstraint("working_hour_id", "lang_code", name="uq_faculty_director_working_hour_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    working_hour_id = Column(
        Integer,
        ForeignKey("faculty_director_working_hours.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    day = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    working_hour = relationship("FacultyDirectorWorkingHour", back_populates="translations")


class FacultyDirectorScientificEvent(Base):
    __tablename__ = "faculty_director_scientific_events"

    id = Column(Integer, primary_key=True, index=True)
    director_id = Column(
        Integer,
        ForeignKey("faculty_directors.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    director = relationship("FacultyDirector", back_populates="scientific_events")
    translations = relationship(
        "FacultyDirectorScientificEventTr",
        back_populates="scientific_event",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class FacultyDirectorScientificEventTr(Base):
    __tablename__ = "faculty_director_scientific_event_tr"
    __table_args__ = (
        UniqueConstraint("scientific_event_id", "lang_code", name="uq_faculty_director_scientific_event_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    scientific_event_id = Column(
        Integer,
        ForeignKey("faculty_director_scientific_events.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    event_title = Column(String(255), nullable=False)
    event_description = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    scientific_event = relationship("FacultyDirectorScientificEvent", back_populates="translations")


class FacultyDirectorEducation(Base):
    __tablename__ = "faculty_director_educations"

    id = Column(Integer, primary_key=True, index=True)
    director_id = Column(
        Integer,
        ForeignKey("faculty_directors.id", ondelete="CASCADE"),
        nullable=False,
    )
    start_year = Column(String(20))
    end_year = Column(String(20))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    director = relationship("FacultyDirector", back_populates="educations")
    translations = relationship(
        "FacultyDirectorEducationTr",
        back_populates="education",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class FacultyDirectorEducationTr(Base):
    __tablename__ = "faculty_director_education_tr"
    __table_args__ = (
        UniqueConstraint("education_id", "lang_code", name="uq_faculty_director_education_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    education_id = Column(
        Integer,
        ForeignKey("faculty_director_educations.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    degree = Column(String(255), nullable=False)
    university = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    education = relationship("FacultyDirectorEducation", back_populates="translations")
