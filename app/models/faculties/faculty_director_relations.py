from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class FacultyDirectorWorkingHour(Base):
    __tablename__ = "faculty_director_working_hours"

    id = Column(Integer, primary_key=True, index=True)
    director_id = Column(
        Integer,
        ForeignKey("faculty_directors.id", ondelete="CASCADE"),
        nullable=False,
    )
    day = Column(String(50), nullable=False)
    time_range = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    director = relationship("FacultyDirector", back_populates="working_hours")


class FacultyDirectorScientificEvent(Base):
    __tablename__ = "faculty_director_scientific_events"

    id = Column(Integer, primary_key=True, index=True)
    director_id = Column(
        Integer,
        ForeignKey("faculty_directors.id", ondelete="CASCADE"),
        nullable=False,
    )
    event_title = Column(String(255), nullable=False)
    event_description = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    director = relationship("FacultyDirector", back_populates="scientific_events")


class FacultyDirectorEducation(Base):
    __tablename__ = "faculty_director_educations"

    id = Column(Integer, primary_key=True, index=True)
    director_id = Column(
        Integer,
        ForeignKey("faculty_directors.id", ondelete="CASCADE"),
        nullable=False,
    )
    degree = Column(String(255), nullable=False)
    university = Column(String(255), nullable=False)
    start_year = Column(String(20))
    end_year = Column(String(20))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    director = relationship("FacultyDirector", back_populates="educations")
