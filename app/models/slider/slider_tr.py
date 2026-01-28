from app.core.database import Base
from sqlalchemy import Column, Integer, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

class SliderTranslation(Base):
    __tablename__ = "slider_translation"

    id = Column(Integer, primary_key=True, index=True)
    slider_id = Column(
        Integer,
        ForeignKey("slider.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(Text(2), nullable=False)
    desc = Column(Text, nullable=False)

    __table_args__ = (
        UniqueConstraint("slider_id", "lang_code", name="uq_slider_translation_lang"),
    )

    slider = relationship("Slider", back_populates="translations")
