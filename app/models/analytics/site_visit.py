from sqlalchemy import BigInteger, CHAR, Column, Date, Index

from app.core.database import Base


class SiteVisitDaily(Base):
    """Aggregate page-view counter, one row per day, incremented via upsert."""

    __tablename__ = "site_visit_daily"

    day = Column(Date, primary_key=True)
    views = Column(BigInteger, nullable=False, default=0, server_default="0")

    __table_args__ = (
        Index("ix_site_visit_daily_day", day.desc()),
    )


class SiteVisitUnique(Base):
    """One row per (day, visitor). The row count for a day is that day's uniques.

    visitor_hash is sha256(salt + client IP + user agent + day). The raw IP and
    user agent are never persisted and the hash rotates daily.
    """

    __tablename__ = "site_visit_unique"

    day = Column(Date, primary_key=True)
    visitor_hash = Column(CHAR(64), primary_key=True)
