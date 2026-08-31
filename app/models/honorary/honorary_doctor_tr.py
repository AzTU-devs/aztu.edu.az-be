from sqlalchemy import Column, Integer, Text, DateTime, String, ForeignKey, func

from app.core.database import Base


class HonoraryDoctorTranslation(Base):
    """One row per language for a honorary doctor.

    `description` is the citation shown under the name on the public card; it is
    optional so a person can be published with a name alone.
    """

    __tablename__ = "honorary_doctor_tr"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(
        Integer, ForeignKey("honorary_doctor.id", ondelete="CASCADE"), nullable=False, index=True
    )
    lang_code = Column(String(2), nullable=False)
    full_name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
