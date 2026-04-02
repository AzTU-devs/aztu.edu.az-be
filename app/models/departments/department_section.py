from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship


class DepartmentObjective(Base):
    __tablename__ = "department_objectives"

    id = Column(Integer, primary_key=True, index=True)
    department_code = Column(
        String(50),
        ForeignKey("departments.department_code", ondelete="CASCADE"),
        nullable=False,
    )
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    department = relationship("Department", back_populates="objectives")
    translations = relationship(
        "DepartmentObjectiveTr",
        back_populates="objective",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class DepartmentObjectiveTr(Base):
    __tablename__ = "department_objective_tr"
    __table_args__ = (
        UniqueConstraint("objective_id", "lang_code", name="uq_department_objective_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    objective_id = Column(
        Integer,
        ForeignKey("department_objectives.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    html_content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    objective = relationship("DepartmentObjective", back_populates="translations")


class DepartmentCoreFunction(Base):
    __tablename__ = "department_core_functions"

    id = Column(Integer, primary_key=True, index=True)
    department_code = Column(
        String(50),
        ForeignKey("departments.department_code", ondelete="CASCADE"),
        nullable=False,
    )
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    department = relationship("Department", back_populates="core_functions")
    translations = relationship(
        "DepartmentCoreFunctionTr",
        back_populates="core_function",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class DepartmentCoreFunctionTr(Base):
    __tablename__ = "department_core_function_tr"
    __table_args__ = (
        UniqueConstraint("core_function_id", "lang_code", name="uq_department_core_function_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    core_function_id = Column(
        Integer,
        ForeignKey("department_core_functions.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    html_content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    core_function = relationship("DepartmentCoreFunction", back_populates="translations")
