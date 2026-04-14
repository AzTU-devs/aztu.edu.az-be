from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship


class ResearchInstitute(Base):
    __tablename__ = "research_institutes"

    id = Column(Integer, primary_key=True, index=True)
    institute_code = Column(String(50), unique=True, nullable=False)
    image = Column(String(1024))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    translations = relationship(
        "ResearchInstituteTr",
        back_populates="institute",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    director = relationship(
        "InstituteDirector",
        back_populates="institute",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    staff = relationship(
        "InstituteStaff",
        back_populates="institute",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class ResearchInstituteTr(Base):
    __tablename__ = "research_institutes_tr"
    __table_args__ = (
        UniqueConstraint("institute_code", "lang_code", name="uq_research_institutes_tr_code_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    institute_code = Column(
        String(50),
        ForeignKey("research_institutes.institute_code", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    name = Column(String(255), nullable=False)
    about_html = Column(Text)
    vision_html = Column(Text)
    mission_html = Column(Text)
    goals_html = Column(Text)
    direction_html = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    institute = relationship("ResearchInstitute", back_populates="translations")


class InstituteDirector(Base):
    __tablename__ = "institute_directors"
    __table_args__ = (
        UniqueConstraint("institute_code", name="uq_institute_directors_code"),
    )

    id = Column(Integer, primary_key=True, index=True)
    institute_code = Column(
        String(50),
        ForeignKey("research_institutes.institute_code", ondelete="CASCADE"),
        nullable=False,
    )
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    father_name = Column(String(100))
    email = Column(String(255))
    room_number = Column(String(50))
    image = Column(String(1024))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    institute = relationship("ResearchInstitute", back_populates="director")
    translations = relationship(
        "InstituteDirectorTr",
        back_populates="director",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    educations = relationship(
        "InstituteDirectorEducation",
        back_populates="director",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class InstituteDirectorTr(Base):
    __tablename__ = "institute_director_tr"
    __table_args__ = (
        UniqueConstraint("director_id", "lang_code", name="uq_institute_director_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    director_id = Column(
        Integer,
        ForeignKey("institute_directors.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    scientific_name = Column(String(255))
    scientific_degree = Column(String(255))
    bio = Column(Text)
    researcher_areas = Column(Text)  # Store as JSON or string? Let's use Text to be safe, or JSONB if using Postgres.
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    director = relationship("InstituteDirector", back_populates="translations")


class InstituteDirectorEducation(Base):
    __tablename__ = "institute_director_educations"

    id = Column(Integer, primary_key=True, index=True)
    director_id = Column(
        Integer,
        ForeignKey("institute_directors.id", ondelete="CASCADE"),
        nullable=False,
    )
    university_name = Column(String(255), nullable=False)
    start_year = Column(String(20))
    end_year = Column(String(20))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    director = relationship("InstituteDirector", back_populates="educations")
    translations = relationship(
        "InstituteDirectorEducationTr",
        back_populates="education",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class InstituteDirectorEducationTr(Base):
    __tablename__ = "institute_director_education_tr"
    __table_args__ = (
        UniqueConstraint("education_id", "lang_code", name="uq_institute_director_education_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    education_id = Column(
        Integer,
        ForeignKey("institute_director_educations.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    degree = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    education = relationship("InstituteDirectorEducation", back_populates="translations")


class InstituteStaff(Base):
    __tablename__ = "institute_staff"

    id = Column(Integer, primary_key=True, index=True)
    institute_code = Column(
        String(50),
        ForeignKey("research_institutes.institute_code", ondelete="CASCADE"),
        nullable=False,
    )
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    father_name = Column(String(100))
    email = Column(String(255))
    phone_number = Column(String(50))
    image = Column(String(1024))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    institute = relationship("ResearchInstitute", back_populates="staff")
    translations = relationship(
        "InstituteStaffTr",
        back_populates="staff",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class InstituteStaffTr(Base):
    __tablename__ = "institute_staff_tr"
    __table_args__ = (
        UniqueConstraint("staff_id", "lang_code", name="uq_institute_staff_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(
        Integer,
        ForeignKey("institute_staff.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    scientific_name = Column(String(255))
    scientific_degree = Column(String(255))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    staff = relationship("InstituteStaff", back_populates="translations")
