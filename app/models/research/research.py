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
    # Which shape this page is: priorities | patents. Drives the dashboard form
    # and, later, the website renderer — the research section will not stay one
    # page.
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
    patent_years = relationship(
        "ResearchPatentYear",
        back_populates="page",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="ResearchPatentYear.display_order",
    )
    seminars = relationship(
        "ResearchSeminar",
        back_populates="page",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="ResearchSeminar.display_order",
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
    # Rich text of the page's one intro card — the "Strateji baxış" block on the
    # priorities page, the paragraph above the tables on the patents page. Both
    # are the same thing structurally: one editor-authored body owned by the
    # page. Whatever heading sits over it is drawn by the website.
    body_html = Column(Text)
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


class ResearchPatentYear(Base):
    """One year heading on the patents page, with its own table under it.

    An explicit row rather than a `year` column on the patent: the page renders
    a heading per year, an editor adds a year and then fills it, and an empty
    year is a legitimate in-progress state. `display_order` records the order
    the dashboard sent them in; the API sorts newest first from the year itself.
    """

    __tablename__ = "research_patent_years"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(
        Integer, ForeignKey("research_pages.id", ondelete="CASCADE"), nullable=False
    )
    # Shown verbatim, and language-neutral: "2024", "2025".
    year = Column(String(50))
    display_order = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    page = relationship("ResearchPage", back_populates="patent_years")
    patents = relationship(
        "ResearchPatent",
        back_populates="year_row",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="ResearchPatent.display_order",
    )


class ResearchPatent(Base):
    """One row of a year's patent table.

    The row number ("№") is not stored — it is the position, and deriving it
    means it can never disagree with the ordering the editor sees.
    """

    __tablename__ = "research_patents"

    id = Column(Integer, primary_key=True, index=True)
    year_id = Column(
        Integer, ForeignKey("research_patent_years.id", ondelete="CASCADE"), nullable=False
    )
    # Registration number, shown verbatim in every language: "İ 2024 0058",
    # "№047247", "WO2023242086".
    patent_number = Column(String(255))
    # The certificate: either an uploaded file's path or a pasted URL (most are
    # Google Drive links today). One column, because the page treats them alike.
    document_url = Column(String(2048))
    display_order = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    year_row = relationship("ResearchPatentYear", back_populates="patents")
    translations = relationship(
        "ResearchPatentTr",
        back_populates="patent",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class ResearchPatentTr(Base):
    __tablename__ = "research_patent_tr"
    __table_args__ = (
        UniqueConstraint("patent_id", "lang_code", name="uq_research_patent_tr_patent_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    patent_id = Column(
        Integer, ForeignKey("research_patents.id", ondelete="CASCADE"), nullable=False
    )
    lang_code = Column(String(10), nullable=False)

    name = Column(Text)
    # One line, as the table renders it: "Rəsulov Nəriman, Məmmədov Ərəstun".
    # Not a child table — the page never addresses an author on their own, and
    # these are free-text credits rather than links to employee records.
    authors = Column(Text)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    patent = relationship("ResearchPatent", back_populates="translations")


class ResearchSeminar(Base):
    """One seminar/training entry on the "Seminarlar və Təlimlər" page.

    Carries no stable key — position is its identity — and links out to the
    matching news item on this website. The ``url`` is language-neutral; the
    ``name`` is bilingual rich text.
    """

    __tablename__ = "research_page_seminars"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(
        Integer, ForeignKey("research_pages.id", ondelete="CASCADE"), nullable=False
    )
    # The news URL this training links to — an absolute or a site-relative path.
    url = Column(String(2048))
    display_order = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    page = relationship("ResearchPage", back_populates="seminars")
    translations = relationship(
        "ResearchSeminarTr",
        back_populates="seminar",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class ResearchSeminarTr(Base):
    __tablename__ = "research_page_seminar_tr"
    __table_args__ = (
        UniqueConstraint("seminar_id", "lang_code", name="uq_research_seminar_tr_seminar_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    seminar_id = Column(
        Integer, ForeignKey("research_page_seminars.id", ondelete="CASCADE"), nullable=False
    )
    lang_code = Column(String(10), nullable=False)

    # The training's name — rich text authored in the dashboard.
    name = Column(Text)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    seminar = relationship("ResearchSeminar", back_populates="translations")


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
