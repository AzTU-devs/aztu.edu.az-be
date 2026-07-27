"""Research section ("Tədqiqat").

The same shape as the About section and for the same reason: a research page is
a hero (title + short description), a body of editor-authored copy, an ordered
list of cards, and an ordered list of "More in this section" buttons. Everything
the website draws by itself — the breadcrumb, the eyebrow, the card icons and
gradients, the counter strip, the SEO tags — is hard-coded there and therefore
has no column here.

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
from sqlalchemy.orm import relationship


class ResearchPage(Base):
    __tablename__ = "research_pages"

    id = Column(Integer, primary_key=True, index=True)
    page_key = Column(String(100), unique=True, nullable=False)
    # Which shape this page is: priorities | … . Drives the dashboard form and,
    # later, the website renderer — the research section will not stay one page.
    template = Column(String(50), nullable=False, default="priorities")
    slug_az = Column(String(255))
    slug_en = Column(String(255))
    display_order = Column(Integer, nullable=False, default=0)
    # False keeps the page out of the public API while it is being filled in.
    is_active = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    translations = relationship(
        "ResearchPageTr",
        back_populates="page",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    priorities = relationship(
        "ResearchPriority",
        back_populates="page",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="ResearchPriority.display_order",
    )
    links = relationship(
        "ResearchPageLink",
        back_populates="page",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="ResearchPageLink.display_order",
    )


class ResearchPageTr(Base):
    __tablename__ = "research_page_tr"
    __table_args__ = (
        UniqueConstraint("page_id", "lang_code", name="uq_research_page_tr_page_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(
        Integer, ForeignKey("research_pages.id", ondelete="CASCADE"), nullable=False
    )
    lang_code = Column(String(10), nullable=False)

    title = Column(String(500))
    # Rich text, rendered under the H1 in the hero.
    description = Column(Text)
    # Rich text of the "Strateji baxış" intro card. The heading itself is drawn
    # by the website, so only the body is stored.
    vision_html = Column(Text)
    # Heading of the "More in this section" block.
    links_title = Column(String(500))

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    page = relationship("ResearchPage", back_populates="translations")


class ResearchPriority(Base):
    """One card in the priority grid.

    Carries no stable key on purpose — the card's number is just its position,
    and the icon that goes with it is chosen by the website from that position.
    """

    __tablename__ = "research_page_priorities"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(
        Integer, ForeignKey("research_pages.id", ondelete="CASCADE"), nullable=False
    )
    display_order = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    page = relationship("ResearchPage", back_populates="priorities")
    translations = relationship(
        "ResearchPriorityTr",
        back_populates="priority",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class ResearchPriorityTr(Base):
    __tablename__ = "research_page_priority_tr"
    __table_args__ = (
        UniqueConstraint(
            "priority_id", "lang_code", name="uq_research_priority_tr_priority_lang"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    priority_id = Column(
        Integer,
        ForeignKey("research_page_priorities.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)

    title = Column(String(500))
    description = Column(Text)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    priority = relationship("ResearchPriority", back_populates="translations")


class ResearchPageLink(Base):
    """One button in the "More in this section" block."""

    __tablename__ = "research_page_links"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(
        Integer, ForeignKey("research_pages.id", ondelete="CASCADE"), nullable=False
    )
    url = Column(String(2048))
    display_order = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    page = relationship("ResearchPage", back_populates="links")
    translations = relationship(
        "ResearchPageLinkTr",
        back_populates="link",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class ResearchPageLinkTr(Base):
    __tablename__ = "research_page_link_tr"
    __table_args__ = (
        UniqueConstraint("link_id", "lang_code", name="uq_research_page_link_tr_link_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    link_id = Column(
        Integer, ForeignKey("research_page_links.id", ondelete="CASCADE"), nullable=False
    )
    lang_code = Column(String(10), nullable=False)

    label = Column(String(500))

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    link = relationship("ResearchPageLink", back_populates="translations")
