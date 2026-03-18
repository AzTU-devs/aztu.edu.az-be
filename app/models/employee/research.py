from app.core.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship


class Research(Base):
    __tablename__ = "employee_research"
    __table_args__ = (
        UniqueConstraint("employee_code", name="uq_employee_research_code"),
    )

    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(
        String(50),
        ForeignKey("employees.employee_code", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    scopus_url = Column(Text, nullable=True)
    google_scholar_url = Column(Text, nullable=True)
    orcid_url = Column(Text, nullable=True)
    researchgate_url = Column(Text, nullable=True)
    academia_url = Column(Text, nullable=True)
    publications = Column(Text, nullable=True)

    employee = relationship("Employee", back_populates="research")
