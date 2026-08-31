from sqlalchemy import Column, Integer, Text, DateTime, Boolean, func

from app.core.database import Base


class HonoraryDoctor(Base):
    """A person awarded an honorary doctorate.

    The roll is unbounded — editors add rows freely — so ordering is explicit
    (`display_order`) rather than derived from the title or the insertion date.
    Everything language-dependent lives in the translation table; only the
    portrait and the ordering flags are shared between languages.
    """

    __tablename__ = "honorary_doctor"

    id = Column(Integer, primary_key=True, index=True)
    image = Column(Text, nullable=True)
    display_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
