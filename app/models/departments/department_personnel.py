from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship


class DepartmentWorker(Base):
    __tablename__ = "department_workers"

    id = Column(Integer, primary_key=True, index=True)
    department_code = Column(
        String(50),
        ForeignKey("departments.department_code", ondelete="CASCADE"),
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

    department = relationship("Department", back_populates="workers")
    translations = relationship(
        "DepartmentWorkerTr",
        back_populates="worker",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class DepartmentWorkerTr(Base):
    __tablename__ = "department_worker_tr"
    __table_args__ = (
        UniqueConstraint("worker_id", "lang_code", name="uq_department_worker_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(
        Integer,
        ForeignKey("department_workers.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    duty = Column(String(255), nullable=False)
    scientific_degree = Column(String(255))
    scientific_name = Column(String(255))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    worker = relationship("DepartmentWorker", back_populates="translations")
