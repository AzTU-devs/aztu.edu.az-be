from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
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
    email = Column(String(255))
    phone = Column(String(50))
    profile_image = Column(String(1024))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    faculty = relationship("Faculty", back_populates="deputy_deans")
    translations = relationship(
        "FacultyDeputyDeanTr",
        back_populates="deputy_dean",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class FacultyDeputyDeanTr(Base):
    __tablename__ = "faculty_deputy_dean_tr"
    __table_args__ = (
        UniqueConstraint("deputy_dean_id", "lang_code", name="uq_faculty_deputy_dean_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    deputy_dean_id = Column(
        Integer,
        ForeignKey("faculty_deputy_deans.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    scientific_name = Column(String(255))
    scientific_degree = Column(String(255))
    duty = Column(String(255))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    deputy_dean = relationship("FacultyDeputyDean", back_populates="translations")


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
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    faculty = relationship("Faculty", back_populates="scientific_council")
    translations = relationship(
        "FacultyCouncilMemberTr",
        back_populates="council_member",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class FacultyCouncilMemberTr(Base):
    __tablename__ = "faculty_council_member_tr"
    __table_args__ = (
        UniqueConstraint("council_member_id", "lang_code", name="uq_faculty_council_member_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    council_member_id = Column(
        Integer,
        ForeignKey("faculty_scientific_council.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    duty = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    council_member = relationship("FacultyCouncilMember", back_populates="translations")


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
    email = Column(String(255))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    faculty = relationship("Faculty", back_populates="workers")
    translations = relationship(
        "FacultyWorkerTr",
        back_populates="worker",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class FacultyWorkerTr(Base):
    __tablename__ = "faculty_worker_tr"
    __table_args__ = (
        UniqueConstraint("worker_id", "lang_code", name="uq_faculty_worker_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(
        Integer,
        ForeignKey("faculty_workers.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    duty = Column(String(255), nullable=False)
    scientific_name = Column(String(255))
    scientific_degree = Column(String(255))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    worker = relationship("FacultyWorker", back_populates="translations")
