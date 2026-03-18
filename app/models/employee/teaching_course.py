import enum
from app.core.database import Base
from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class EducationLevel(str, enum.Enum):
    bachelor = "bachelor"
    master = "master"


class TeachingCourse(Base):
    __tablename__ = "teaching_courses"

    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(
        String(50),
        ForeignKey("employees.employee_code", ondelete="CASCADE"),
        nullable=False,
    )
    education_level = Column(Enum(EducationLevel, name="education_level_enum"), nullable=False)

    employee = relationship("Employee", back_populates="courses")
    translations = relationship(
        "TeachingCourseTr",
        back_populates="course",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
