import enum
from app.core.database import Base
from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class DegreeLevel(str, enum.Enum):
    Bachelor = "Bachelor"
    Master = "Master"
    PhD = "PhD"


class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(
        String(50),
        ForeignKey("employees.employee_code", ondelete="CASCADE"),
        nullable=False,
    )
    degree_level = Column(Enum(DegreeLevel, name="degree_level_enum"), nullable=False)
    institution = Column(String(255), nullable=False)
    specialization = Column(String(255), nullable=True)
    graduation_year = Column(Integer, nullable=True)

    employee = relationship("Employee", back_populates="educations")
