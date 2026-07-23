"""About section ("Haqqımızda").

A page is a hero (title + short description), an ordered list of statement
cards, and an ordered list of "More in this section" buttons. That is the whole
shape — the hero video, the card icons and the SEO tags are hard-coded in the
website, so they deliberately have no columns here.

Language-neutral facts (a slug, a URL, an ordering) live on the row; anything a
translator would touch lives on the ``*_tr`` sibling keyed by ``lang_code``.
"""

from app.core.database import Base
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship


class AboutPage(Base):
    __tablename__ = "about_pages"

    id = Column(Integer, primary_key=True, index=True)
    page_key = Column(String(100), unique=True, nullable=False)
    # Which shape this page is: statements | timeline. Drives the dashboard
    # form and, later, the website renderer.
    template = Column(String(50), nullable=False, default="statements")
    slug_az = Column(String(255))
    slug_en = Column(String(255))
    # The downloadable plan: either an uploaded file's path or a pasted URL.
    # One column, because from the page's point of view they are the same thing.
    document_url = Column(String(2048))
    display_order = Column(Integer, nullable=False, default=0)
    # False keeps the page out of the public API while it is being filled in.
    is_active = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    translations = relationship(
        "AboutPageTr",
        back_populates="page",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    blocks = relationship(
        "AboutBlock",
        back_populates="page",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="AboutBlock.display_order",
    )
    links = relationship(
        "AboutLink",
        back_populates="page",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="AboutLink.display_order",
    )
    pillars = relationship(
        "AboutPillar",
        back_populates="page",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="AboutPillar.display_order",
    )
    lists = relationship(
        "AboutList",
        back_populates="page",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="AboutList.display_order",
    )
    milestones = relationship(
        "AboutMilestone",
        back_populates="page",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="AboutMilestone.display_order",
    )


class AboutPageTr(Base):
    __tablename__ = "about_page_tr"
    __table_args__ = (
        UniqueConstraint("page_id", "lang_code", name="uq_about_page_tr_page_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("about_pages.id", ondelete="CASCADE"), nullable=False)
    lang_code = Column(String(10), nullable=False)

    title = Column(String(500))
    # Rich text, rendered under the H1 in the hero.
    description = Column(Text)
    # Heading of the "More in this section" block.
    links_title = Column(String(500))
    # Text on the document download button.
    document_label = Column(String(500))
    # Heading above the pillar cards.
    pillars_title = Column(String(500))

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    page = relationship("AboutPage", back_populates="translations")


class AboutBlock(Base):
    """A statement card — Mission, Vision or Goal."""

    __tablename__ = "about_blocks"
    __table_args__ = (
        UniqueConstraint("page_id", "block_key", name="uq_about_blocks_page_key"),
    )

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("about_pages.id", ondelete="CASCADE"), nullable=False)
    # Stable identifier the website maps to an icon: mission | vision | goal.
    block_key = Column(String(100), nullable=False)
    display_order = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    page = relationship("AboutPage", back_populates="blocks")
    translations = relationship(
        "AboutBlockTr",
        back_populates="block",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class AboutBlockTr(Base):
    __tablename__ = "about_block_tr"
    __table_args__ = (
        UniqueConstraint("block_id", "lang_code", name="uq_about_block_tr_block_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    block_id = Column(Integer, ForeignKey("about_blocks.id", ondelete="CASCADE"), nullable=False)
    lang_code = Column(String(10), nullable=False)

    title = Column(String(500))
    body = Column(Text)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    block = relationship("AboutBlock", back_populates="translations")


class AboutLink(Base):
    """One button in the "More in this section" block."""

    __tablename__ = "about_links"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("about_pages.id", ondelete="CASCADE"), nullable=False)
    url = Column(String(2048))
    display_order = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    page = relationship("AboutPage", back_populates="links")
    translations = relationship(
        "AboutLinkTr",
        back_populates="link",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class AboutLinkTr(Base):
    __tablename__ = "about_link_tr"
    __table_args__ = (
        UniqueConstraint("link_id", "lang_code", name="uq_about_link_tr_link_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    link_id = Column(Integer, ForeignKey("about_links.id", ondelete="CASCADE"), nullable=False)
    lang_code = Column(String(10), nullable=False)

    label = Column(String(500))

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    link = relationship("AboutLink", back_populates="translations")


class AboutMilestone(Base):
    """One year on the history timeline."""

    __tablename__ = "about_milestones"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("about_pages.id", ondelete="CASCADE"), nullable=False)
    # Shown verbatim: "1950", "1887-1905", "Bu gün". Text, because the timeline
    # ends on a non-numeric entry — ordering is decided in the service.
    year = Column(String(50))
    # Tie-break only; the API orders by the year itself, newest first.
    display_order = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    page = relationship("AboutPage", back_populates="milestones")
    translations = relationship(
        "AboutMilestoneTr",
        back_populates="milestone",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class AboutMilestoneTr(Base):
    __tablename__ = "about_milestone_tr"
    __table_args__ = (
        UniqueConstraint("milestone_id", "lang_code", name="uq_about_milestone_tr_ms_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    milestone_id = Column(
        Integer, ForeignKey("about_milestones.id", ondelete="CASCADE"), nullable=False
    )
    lang_code = Column(String(10), nullable=False)

    title = Column(String(500))
    description = Column(Text)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    milestone = relationship("AboutMilestone", back_populates="translations")


class AboutPillar(Base):
    """One numbered card under "Strateji Sütunlar"."""

    __tablename__ = "about_pillars"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("about_pages.id", ondelete="CASCADE"), nullable=False)
    display_order = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    page = relationship("AboutPage", back_populates="pillars")
    translations = relationship(
        "AboutPillarTr",
        back_populates="pillar",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class AboutPillarTr(Base):
    __tablename__ = "about_pillar_tr"
    __table_args__ = (
        UniqueConstraint("pillar_id", "lang_code", name="uq_about_pillar_tr_pillar_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    pillar_id = Column(Integer, ForeignKey("about_pillars.id", ondelete="CASCADE"), nullable=False)
    lang_code = Column(String(10), nullable=False)

    title = Column(String(500))
    description = Column(Text)
    # Ordered plain strings — the chips under the card.
    tags = Column(JSONB)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    pillar = relationship("AboutPillar", back_populates="translations")


class AboutList(Base):
    """A heading plus an ordered set of one-line entries.

    Used twice on the strategic plan — the corporate values (bulleted) and the
    KPIs (numbered). `style` is the only thing that differs.
    """

    __tablename__ = "about_lists"
    __table_args__ = (
        UniqueConstraint("page_id", "list_key", name="uq_about_lists_page_key"),
    )

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("about_pages.id", ondelete="CASCADE"), nullable=False)
    list_key = Column(String(100), nullable=False)
    # bullet | number
    style = Column(String(20), nullable=False, default="bullet")
    display_order = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    page = relationship("AboutPage", back_populates="lists")
    translations = relationship(
        "AboutListTr",
        back_populates="list",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class AboutListTr(Base):
    __tablename__ = "about_list_tr"
    __table_args__ = (
        UniqueConstraint("list_id", "lang_code", name="uq_about_list_tr_list_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    list_id = Column(Integer, ForeignKey("about_lists.id", ondelete="CASCADE"), nullable=False)
    lang_code = Column(String(10), nullable=False)

    title = Column(String(500))
    # Ordered plain strings, one per rendered line.
    items = Column(JSONB)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    list = relationship("AboutList", back_populates="translations")
