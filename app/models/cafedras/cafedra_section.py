from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship


class CafedraDirectionOfAction(Base):
    __tablename__ = "cafedra_directions_of_action"

    id = Column(Integer, primary_key=True, index=True)
    cafedra_code = Column(
        String(50),
        ForeignKey("cafedras.cafedra_code", ondelete="CASCADE"),
        nullable=False,
    )
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    cafedra = relationship("Cafedra", back_populates="directions_of_action")
    translations = relationship(
        "CafedraDirectionOfActionTr",
        back_populates="direction_of_action",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class CafedraDirectionOfActionTr(Base):
    __tablename__ = "cafedra_direction_of_action_tr"
    __table_args__ = (
        UniqueConstraint("direction_of_action_id", "lang_code", name="uq_cafedra_doa_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    direction_of_action_id = Column(
        Integer,
        ForeignKey("cafedra_directions_of_action.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    direction_of_action = relationship("CafedraDirectionOfAction", back_populates="translations")
