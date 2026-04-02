from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship


class DepartmentDirector(Base):
    __tablename__ = "department_directors"
    __table_args__ = (
        UniqueConstraint("department_code", name="uq_department_directors_code"),
    )

    id = Column(Integer, primary_key=True, index=True)
    department_code = Column(
        String(50),
        ForeignKey("departments.department_code", ondelete="CASCADE"),
        nullable=False,
    )
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    father_name = Column(String(100))
    room_number = Column(String(50))
    profile_image = Column(String(1024))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    department = relationship("Department", back_populates="director")
    translations = relationship(
        "DepartmentDirectorTr",
        back_populates="director",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    working_hours = relationship(
        "DepartmentDirectorWorkingHour",
        back_populates="director",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    educations = relationship(
        "DepartmentDirectorEducation",
        back_populates="director",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class DepartmentDirectorTr(Base):
    __tablename__ = "department_director_tr"
    __table_args__ = (
        UniqueConstraint("director_id", "lang_code", name="uq_department_director_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    director_id = Column(
        Integer,
        ForeignKey("department_directors.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    scientific_degree = Column(String(255))
    scientific_title = Column(String(255))
    bio = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    director = relationship("DepartmentDirector", back_populates="translations")


class DepartmentDirectorWorkingHour(Base):
    __tablename__ = "department_director_working_hours"

    id = Column(Integer, primary_key=True, index=True)
    director_id = Column(
        Integer,
        ForeignKey("department_directors.id", ondelete="CASCADE"),
        nullable=False,
    )
    time_range = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    director = relationship("DepartmentDirector", back_populates="working_hours")
    translations = relationship(
        "DepartmentDirectorWorkingHourTr",
        back_populates="working_hour",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class DepartmentDirectorWorkingHourTr(Base):
    __tablename__ = "department_director_working_hour_tr"
    __table_args__ = (
        UniqueConstraint("working_hour_id", "lang_code", name="uq_department_director_working_hour_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    working_hour_id = Column(
        Integer,
        ForeignKey("department_director_working_hours.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    day = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    working_hour = relationship("DepartmentDirectorWorkingHour", back_populates="translations")


class DepartmentDirectorEducation(Base):
    __tablename__ = "department_director_educations"

    id = Column(Integer, primary_key=True, index=True)
    director_id = Column(
        Integer,
        ForeignKey("department_directors.id", ondelete="CASCADE"),
        nullable=False,
    )
    start_year = Column(String(20))
    end_year = Column(String(20))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    director = relationship("DepartmentDirector", back_populates="educations")
    translations = relationship(
        "DepartmentDirectorEducationTr",
        back_populates="education",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class DepartmentDirectorEducationTr(Base):
    __tablename__ = "department_director_education_tr"
    __table_args__ = (
        UniqueConstraint("education_id", "lang_code", name="uq_department_director_education_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    education_id = Column(
        Integer,
        ForeignKey("department_director_educations.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    degree = Column(String(255), nullable=False)
    university = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    education = relationship("DepartmentDirectorEducation", back_populates="translations")
