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

    # ── Rector-page (template = "rector") columns ────────────────────────────
    # Language-neutral facts about the person the page is about. They live on
    # the row, not the ``*_tr`` sibling, because "30+ Years", an email and a
    # portrait read the same in every language.
    experience = Column(String(100))
    email = Column(String(255))
    # The rector's portrait: an uploaded file's path or a pasted URL, like
    # ``document_url``.
    image_url = Column(String(2048))

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
    persons = relationship(
        "AboutPerson",
        back_populates="page",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="AboutPerson.display_order",
    )
    milestones = relationship(
        "AboutMilestone",
        back_populates="page",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="AboutMilestone.display_order",
    )
    councils = relationship(
        "AboutCouncil",
        back_populates="page",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="AboutCouncil.display_order",
    )
    doc_categories = relationship(
        "AboutDocCategory",
        back_populates="page",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="AboutDocCategory.display_order",
    )
    documents = relationship(
        "AboutDocument",
        back_populates="page",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="AboutDocument.display_order",
    )
    images = relationship(
        "AboutImage",
        back_populates="page",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="AboutImage.display_order",
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
    # Comma/·-separated category line for the vice-rector hero.
    domains = Column(Text)
    # The page's second heading ("Executive Leadership") and its lead.
    section_title = Column(String(500))
    section_body = Column(Text)
    # Heading above the councils list on the scientific-board page.
    councils_title = Column(String(500))

    # ── Rector-page (template = "rector") translations ───────────────────────
    # The rector's academic degree ("Technical Sciences") and title
    # ("Professor") — short strings shown in the hero stat cards.
    degree = Column(String(255))
    position = Column(String(255))
    # Rich text: the rector's full message (the editor keeps line spacing) and
    # the "About the rector" biography.
    message = Column(Text)
    about = Column(Text)

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


class AboutImage(Base):
    """One picture in a page's gallery — used by the rector page.

    Images are language-neutral, so there is no ``*_tr`` sibling: the row is
    just a stored file (or pasted URL) and its position in the strip.
    """

    __tablename__ = "about_images"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("about_pages.id", ondelete="CASCADE"), nullable=False)
    # An uploaded file's path or a pasted URL — the page treats them alike.
    image_url = Column(String(2048), nullable=False)
    display_order = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    page = relationship("AboutPage", back_populates="images")


class AboutPerson(Base):
    """A vice-rector card, with its own detail ("see profile") copy."""

    __tablename__ = "about_persons"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("about_pages.id", ondelete="CASCADE"), nullable=False)
    email = Column(String(255))
    phone = Column(String(100))
    # Optional internal extension.
    phone_code = Column(String(50))
    # Portrait: an uploaded file's path or a pasted URL.
    image_url = Column(String(2048))
    # Former-rectors page: the years the person held office. Language-neutral
    # free text ("1950", "1955") — a year reads the same in both languages.
    year_start = Column(String(20))
    year_end = Column(String(20))
    display_order = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    page = relationship("AboutPage", back_populates="persons")
    translations = relationship(
        "AboutPersonTr",
        back_populates="person",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class AboutPersonTr(Base):
    __tablename__ = "about_person_tr"
    __table_args__ = (
        UniqueConstraint("person_id", "lang_code", name="uq_about_person_tr_person_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("about_persons.id", ondelete="CASCADE"), nullable=False)
    lang_code = Column(String(10), nullable=False)

    # "Prof. Subhan Namazov" — name with scientific title prefix.
    name = Column(String(500))
    # Family name, kept separate on the former-rectors page and for a partner
    # institution's director. Vice-rectors leave it null (the name carries all).
    surname = Column(String(500))
    # "Doctor of Technical Sciences, Professor".
    degree = Column(String(500))
    # "Vice-Rector for Academic Affairs".
    position = Column(String(500))
    # The long profile behind the card's "see profile" button — rich text.
    bio = Column(Text)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    person = relationship("AboutPerson", back_populates="translations")


class AboutCouncil(Base):
    """One council on the scientific-board page.

    A page carries an unlimited, ordered list of councils; each council owns a
    bilingual name and two rosters of people — its members and its secretariat —
    which live on ``AboutCouncilMember`` keyed by ``role``.
    """

    __tablename__ = "about_councils"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("about_pages.id", ondelete="CASCADE"), nullable=False)
    display_order = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    page = relationship("AboutPage", back_populates="councils")
    translations = relationship(
        "AboutCouncilTr",
        back_populates="council",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    members = relationship(
        "AboutCouncilMember",
        back_populates="council",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="AboutCouncilMember.display_order",
    )


class AboutCouncilTr(Base):
    __tablename__ = "about_council_tr"
    __table_args__ = (
        UniqueConstraint("council_id", "lang_code", name="uq_about_council_tr_council_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    council_id = Column(
        Integer, ForeignKey("about_councils.id", ondelete="CASCADE"), nullable=False
    )
    lang_code = Column(String(10), nullable=False)

    # "Böyük Elmi Şura" / "Grand Scientific Council".
    name = Column(String(500))

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    council = relationship("AboutCouncil", back_populates="translations")


class AboutCouncilMember(Base):
    """One person on a council — either a member or a secretariat member.

    ``role`` is the discriminator ("member" | "secretary"); a name, surname and
    duty read differently per language, so they live on the ``*_tr`` sibling.
    """

    __tablename__ = "about_council_members"

    id = Column(Integer, primary_key=True, index=True)
    council_id = Column(
        Integer, ForeignKey("about_councils.id", ondelete="CASCADE"), nullable=False
    )
    # Which roster this row belongs to: member | secretary.
    role = Column(String(20), nullable=False, default="member")
    display_order = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    council = relationship("AboutCouncil", back_populates="members")
    translations = relationship(
        "AboutCouncilMemberTr",
        back_populates="member",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class AboutCouncilMemberTr(Base):
    __tablename__ = "about_council_member_tr"
    __table_args__ = (
        UniqueConstraint(
            "member_id", "lang_code", name="uq_about_council_member_tr_member_lang"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(
        Integer, ForeignKey("about_council_members.id", ondelete="CASCADE"), nullable=False
    )
    lang_code = Column(String(10), nullable=False)

    name = Column(String(255))
    surname = Column(String(255))
    # The person's duty on the council ("Chair", "Secretary").
    position = Column(String(500))

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    member = relationship("AboutCouncilMember", back_populates="translations")


class AboutDocCategory(Base):
    """A document category on a regulatory-documents page.

    Categories are defined once per page and a document points at one by its
    stable ``category_key`` (assigned in the dashboard). A page with no
    categories — the sustainability page — simply has none.
    """

    __tablename__ = "about_doc_categories"
    __table_args__ = (
        UniqueConstraint("page_id", "category_key", name="uq_about_doc_categories_page_key"),
    )

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("about_pages.id", ondelete="CASCADE"), nullable=False)
    # Stable, page-local identifier a document references (e.g. "c-ab12cd").
    category_key = Column(String(100), nullable=False)
    display_order = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    page = relationship("AboutPage", back_populates="doc_categories")
    translations = relationship(
        "AboutDocCategoryTr",
        back_populates="category",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class AboutDocCategoryTr(Base):
    __tablename__ = "about_doc_category_tr"
    __table_args__ = (
        UniqueConstraint("category_id", "lang_code", name="uq_about_doc_category_tr_cat_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(
        Integer, ForeignKey("about_doc_categories.id", ondelete="CASCADE"), nullable=False
    )
    lang_code = Column(String(10), nullable=False)

    name = Column(String(500))

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    category = relationship("AboutDocCategory", back_populates="translations")


class AboutDocument(Base):
    """One downloadable document card on a regulatory-documents page.

    The file itself is either an uploaded path or a pasted URL (any format),
    held in ``file_url``. ``category_key`` is optional — it ties the card to one
    of the page's categories where the page has them.
    """

    __tablename__ = "about_documents"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("about_pages.id", ondelete="CASCADE"), nullable=False)
    # References an AboutDocCategory.category_key on the same page, or null.
    category_key = Column(String(100))
    # An uploaded file's path or a pasted URL — the page treats them alike.
    file_url = Column(String(2048))
    display_order = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    page = relationship("AboutPage", back_populates="documents")
    translations = relationship(
        "AboutDocumentTr",
        back_populates="document",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class AboutDocumentTr(Base):
    __tablename__ = "about_document_tr"
    __table_args__ = (
        UniqueConstraint("document_id", "lang_code", name="uq_about_document_tr_doc_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(
        Integer, ForeignKey("about_documents.id", ondelete="CASCADE"), nullable=False
    )
    lang_code = Column(String(10), nullable=False)

    # The document's display name ("Etik Davranış Qaydaları").
    name = Column(String(500))

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    document = relationship("AboutDocument", back_populates="translations")
