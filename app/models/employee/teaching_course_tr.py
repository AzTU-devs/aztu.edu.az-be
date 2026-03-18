from app.core.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship


class TeachingCourseTr(Base):
    __tablename__ = "teaching_course_tr"
    __table_args__ = (
        UniqueConstraint("course_id", "lang_code", name="uq_teaching_course_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(
        Integer,
        ForeignKey("teaching_courses.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    course_name = Column(String(255), nullable=False)

    course = relationship("TeachingCourse", back_populates="translations")
