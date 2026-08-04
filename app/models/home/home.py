"""Home section ("Ana səhifə") — the landing page's metric strips.

The homepage shows two ordered rows of numbers: a compact "hero" strip of
headline rankings (QS, THE, GreenMetric, Accreditation) and a longer "numbers"
grid (faculties, students, staff …). Both are the same shape — a value, a
suffix and a bilingual label — so they live on one table, told apart by a
neutral ``group`` column ("hero" | "numbers").

Language-neutral facts (the value, the "+" suffix, the ordering) live on the
row; anything a translator would touch (label, sublabel) lives on the ``*_tr``
sibling keyed by ``lang_code``.
"""

from app.core.database import Base
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship


class HomePage(Base):
    __tablename__ = "home_pages"

    id = Column(Integer, primary_key=True, index=True)
    page_key = Column(String(100), unique=True, nullable=False)
    # False keeps the page out of the public API while it is being filled in.
    is_active = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    metrics = relationship(
        "HomeMetric",
        back_populates="page",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="HomeMetric.display_order",
    )


class HomeMetric(Base):
    """One number on the homepage — a hero ranking or a "by the numbers" tile."""

    __tablename__ = "home_metrics"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("home_pages.id", ondelete="CASCADE"), nullable=False)
    # Which strip this metric belongs to: hero | numbers.
    group = Column(String(20), nullable=False)
    # The figure itself ("801", "10000") and its trailing mark ("+", "").
    value = Column(String(50))
    suffix = Column(String(20))
    display_order = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    page = relationship("HomePage", back_populates="metrics")
    translations = relationship(
        "HomeMetricTr",
        back_populates="metric",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class HomeMetricTr(Base):
    __tablename__ = "home_metric_tr"
    __table_args__ = (
        UniqueConstraint("metric_id", "lang_code", name="uq_home_metric_tr_metric_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    metric_id = Column(
        Integer, ForeignKey("home_metrics.id", ondelete="CASCADE"), nullable=False
    )
    lang_code = Column(String(10), nullable=False)

    label = Column(String(500))
    # Used by the "numbers" group; null/empty for "hero".
    sublabel = Column(String(500))

    metric = relationship("HomeMetric", back_populates="translations")
