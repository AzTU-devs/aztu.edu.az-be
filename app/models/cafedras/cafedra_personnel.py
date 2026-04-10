from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship


class CafedraWorker(Base):
    __tablename__ = "cafedra_workers"

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
    profile_image = Column(String(1024))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    cafedra = relationship("Cafedra", back_populates="workers")
    translations = relationship(
        "CafedraWorkerTr",
        back_populates="worker",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class CafedraWorkerTr(Base):
    __tablename__ = "cafedra_worker_tr"
    __table_args__ = (
        UniqueConstraint("worker_id", "lang_code", name="uq_cafedra_worker_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(
        Integer,
        ForeignKey("cafedra_workers.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    duty = Column(String(255), nullable=False)
    scientific_name = Column(String(255))
    scientific_degree = Column(String(255))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    worker = relationship("CafedraWorker", back_populates="translations")


class CafedraDeputyDirector(Base):
    __tablename__ = "cafedra_deputy_directors"

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
    profile_image = Column(String(1024))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    cafedra = relationship("Cafedra", back_populates="deputy_directors")
    translations = relationship(
        "CafedraDeputyDirectorTr",
        back_populates="deputy_director",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class CafedraDeputyDirectorTr(Base):
    __tablename__ = "cafedra_deputy_director_tr"
    __table_args__ = (
        UniqueConstraint("deputy_director_id", "lang_code", name="uq_cafedra_deputy_director_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    deputy_director_id = Column(
        Integer,
        ForeignKey("cafedra_deputy_directors.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    scientific_name = Column(String(255))
    scientific_degree = Column(String(255))
    duty = Column(String(255))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    deputy_director = relationship("CafedraDeputyDirector", back_populates="translations")


class CafedraCouncilMember(Base):
    __tablename__ = "cafedra_scientific_council"

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
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    cafedra = relationship("Cafedra", back_populates="scientific_council")
    translations = relationship(
        "CafedraCouncilMemberTr",
        back_populates="council_member",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class CafedraCouncilMemberTr(Base):
    __tablename__ = "cafedra_council_member_tr"
    __table_args__ = (
        UniqueConstraint("council_member_id", "lang_code", name="uq_cafedra_council_member_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    council_member_id = Column(
        Integer,
        ForeignKey("cafedra_scientific_council.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    duty = Column(String(255), nullable=False)
    scientific_name = Column(String(255))
    scientific_degree = Column(String(255))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    council_member = relationship("CafedraCouncilMember", back_populates="translations")
