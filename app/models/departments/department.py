from app.core.database import Base
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    department_code = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    translations = relationship(
        "DepartmentTr",
        back_populates="department",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    director = relationship(
        "DepartmentDirector",
        back_populates="department",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    objectives = relationship(
        "DepartmentObjective",
        back_populates="department",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    core_functions = relationship(
        "DepartmentCoreFunction",
        back_populates="department",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    workers = relationship(
        "DepartmentWorker",
        back_populates="department",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
