from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, JSON
from sqlalchemy.orm import relationship


class CafedraDirector(Base):
    __tablename__ = "cafedra_directors"
    __table_args__ = (
        UniqueConstraint("cafedra_code", name="uq_cafedra_directors_code"),
    )

    id = Column(Integer, primary_key=True, index=True)
    cafedra_code = Column(
        String(50),
        ForeignKey("cafedras.cafedra_code", ondelete="CASCADE"),
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

    cafedra = relationship("Cafedra", back_populates="director")
    translations = relationship(
        "CafedraDirectorTr",
        back_populates="director",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    working_hours = relationship(
        "CafedraDirectorWorkingHour",
        back_populates="director",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    educations = relationship(
        "CafedraDirectorEducation",
        back_populates="director",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class CafedraDirectorTr(Base):
    __tablename__ = "cafedra_director_tr"
    __table_args__ = (
        UniqueConstraint("director_id", "lang_code", name="uq_cafedra_director_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    director_id = Column(
        Integer,
        ForeignKey("cafedra_directors.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    scientific_degree = Column(String(255))
    scientific_title = Column(String(255))
    bio = Column(Text)
    scientific_research_fields = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    director = relationship("CafedraDirector", back_populates="translations")


class CafedraDirectorWorkingHour(Base):
    __tablename__ = "cafedra_director_working_hours"

    id = Column(Integer, primary_key=True, index=True)
    director_id = Column(
        Integer,
        ForeignKey("cafedra_directors.id", ondelete="CASCADE"),
        nullable=False,
    )
    time_range = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    director = relationship("CafedraDirector", back_populates="working_hours")
    translations = relationship(
        "CafedraDirectorWorkingHourTr",
        back_populates="working_hour",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class CafedraDirectorWorkingHourTr(Base):
    __tablename__ = "cafedra_director_working_hour_tr"
    __table_args__ = (
        UniqueConstraint("working_hour_id", "lang_code", name="uq_cafedra_director_working_hour_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    working_hour_id = Column(
        Integer,
        ForeignKey("cafedra_director_working_hours.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    day = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    working_hour = relationship("CafedraDirectorWorkingHour", back_populates="translations")


class CafedraDirectorEducation(Base):
    __tablename__ = "cafedra_director_educations"

    id = Column(Integer, primary_key=True, index=True)
    director_id = Column(
        Integer,
        ForeignKey("cafedra_directors.id", ondelete="CASCADE"),
        nullable=False,
    )
    start_year = Column(String(20))
    end_year = Column(String(20))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    director = relationship("CafedraDirector", back_populates="educations")
    translations = relationship(
        "CafedraDirectorEducationTr",
        back_populates="education",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class CafedraDirectorEducationTr(Base):
    __tablename__ = "cafedra_director_education_tr"
    __table_args__ = (
        UniqueConstraint("education_id", "lang_code", name="uq_cafedra_director_education_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    education_id = Column(
        Integer,
        ForeignKey("cafedra_director_educations.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    degree = Column(String(255), nullable=False)
    university = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    education = relationship("CafedraDirectorEducation", back_populates="translations")
