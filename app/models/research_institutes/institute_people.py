from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship


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
    full_name = Column(String(255), nullable=False)
    email = Column(String(255))
    office = Column(String(100))
    image_url = Column(String(1024))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    institute = relationship("ResearchInstitute", back_populates="director")
    translations = relationship(
        "InstituteDirectorTr",
        back_populates="director",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    research_areas = relationship(
        "DirectorResearchArea",
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
    title = Column(String(255))
    biography = Column(Text)
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
    start_year = Column(String(50))
    end_year = Column(String(50))  # Null/Empty means "present"
    display_order = Column(Integer, default=0)
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
        UniqueConstraint("education_id", "lang_code", name="uq_director_edu_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    education_id = Column(
        Integer,
        ForeignKey("institute_director_educations.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    university = Column(String(255), nullable=False)
    degree = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    education = relationship("InstituteDirectorEducation", back_populates="translations")


class DirectorResearchArea(Base):
    __tablename__ = "director_research_areas"

    id = Column(Integer, primary_key=True, index=True)
    director_id = Column(
        Integer,
        ForeignKey("institute_directors.id", ondelete="CASCADE"),
        nullable=False,
    )
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    director = relationship("InstituteDirector", back_populates="research_areas")
    translations = relationship(
        "DirectorResearchAreaTr",
        back_populates="research_area",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class DirectorResearchAreaTr(Base):
    __tablename__ = "director_research_area_tr"
    __table_args__ = (
        UniqueConstraint("research_area_id", "lang_code", name="uq_director_ra_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    research_area_id = Column(
        Integer,
        ForeignKey("director_research_areas.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    research_area = relationship("DirectorResearchArea", back_populates="translations")


class InstituteStaff(Base):
    __tablename__ = "institute_staff"

    id = Column(Integer, primary_key=True, index=True)
    institute_code = Column(
        String(50),
        ForeignKey("research_institutes.institute_code", ondelete="CASCADE"),
        nullable=False,
    )
    full_name = Column(String(255), nullable=False)
    email = Column(String(255))
    phone = Column(String(50))
    image_url = Column(String(1024))
    display_order = Column(Integer, default=0)
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
    title = Column(String(255))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    staff = relationship("InstituteStaff", back_populates="translations")
