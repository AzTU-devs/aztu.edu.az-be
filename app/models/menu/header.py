from app.core.database import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class MenuHeader(Base):
    """Top-level navigation item (main title shown in the header bar).

    - Can either have a direct_url (leaf – no items allowed) or
      a list of MenuHeaderItems (dropdown).
    - Carries an optional image and per-language translations with
      auto-generated slugs.
    """
    __tablename__ = "menu_headers"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(Text, nullable=True)
    direct_url = Column(String(500), nullable=True)
    display_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    translations = relationship(
        "MenuHeaderTranslation",
        back_populates="header",
        cascade="all, delete-orphan",
    )
    items = relationship(
        "MenuHeaderItem",
        back_populates="header",
        cascade="all, delete-orphan",
    )


class MenuHeaderTranslation(Base):
    __tablename__ = "menu_header_translations"

    id = Column(Integer, primary_key=True, index=True)
    header_id = Column(
        Integer, ForeignKey("menu_headers.id", ondelete="CASCADE"), nullable=False
    )
    lang_code = Column(String(5), nullable=False)   # "az" | "en"
    title = Column(String(200), nullable=False)
    slug = Column(String(200), nullable=False)       # auto-generated from title

    header = relationship("MenuHeader", back_populates="translations")


class MenuHeaderItem(Base):
    """First-level dropdown item under a MenuHeader.

    - Can either have a direct_url (leaf) or a list of MenuHeaderSubItems.
    """
    __tablename__ = "menu_header_items"

    id = Column(Integer, primary_key=True, index=True)
    header_id = Column(
        Integer, ForeignKey("menu_headers.id", ondelete="CASCADE"), nullable=False
    )
    direct_url = Column(String(500), nullable=True)
    display_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    header = relationship("MenuHeader", back_populates="items")
    translations = relationship(
        "MenuHeaderItemTranslation",
        back_populates="item",
        cascade="all, delete-orphan",
    )
    sub_items = relationship(
        "MenuHeaderSubItem",
        back_populates="item",
        cascade="all, delete-orphan",
    )


class MenuHeaderItemTranslation(Base):
    __tablename__ = "menu_header_item_translations"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(
        Integer, ForeignKey("menu_header_items.id", ondelete="CASCADE"), nullable=False
    )
    lang_code = Column(String(5), nullable=False)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), nullable=False)

    item = relationship("MenuHeaderItem", back_populates="translations")


class MenuHeaderSubItem(Base):
    """Second-level (leaf) item under a MenuHeaderItem.

    Always carries a direct_url – no further nesting.
    """
    __tablename__ = "menu_header_sub_items"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(
        Integer, ForeignKey("menu_header_items.id", ondelete="CASCADE"), nullable=False
    )
    direct_url = Column(String(500), nullable=False)
    display_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    item = relationship("MenuHeaderItem", back_populates="sub_items")
    translations = relationship(
        "MenuHeaderSubItemTranslation",
        back_populates="sub_item",
        cascade="all, delete-orphan",
    )


class MenuHeaderSubItemTranslation(Base):
    __tablename__ = "menu_header_sub_item_translations"

    id = Column(Integer, primary_key=True, index=True)
    sub_item_id = Column(
        Integer, ForeignKey("menu_header_sub_items.id", ondelete="CASCADE"), nullable=False
    )
    lang_code = Column(String(5), nullable=False)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), nullable=False)

    sub_item = relationship("MenuHeaderSubItem", back_populates="translations")
