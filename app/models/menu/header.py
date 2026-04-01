from app.core.database import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class MenuHeaderSection(Base):
    __tablename__ = "menu_header_sections"

    id = Column(Integer, primary_key=True, index=True)
    section_key = Column(String(50), unique=True, nullable=False)
    image_url = Column(Text, nullable=False)
    display_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    translations = relationship("MenuHeaderSectionTranslation", back_populates="section", cascade="all, delete-orphan")
    items = relationship("MenuHeaderItem", back_populates="section", cascade="all, delete-orphan")


class MenuHeaderSectionTranslation(Base):
    __tablename__ = "menu_header_section_translations"

    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("menu_header_sections.id", ondelete="CASCADE"), nullable=False)
    lang_code = Column(String(5), nullable=False)
    label = Column(String(100), nullable=False)
    base_path = Column(String(200), nullable=False)

    section = relationship("MenuHeaderSection", back_populates="translations")


class MenuHeaderItem(Base):
    __tablename__ = "menu_header_items"

    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("menu_header_sections.id", ondelete="CASCADE"), nullable=False)
    item_type = Column(String(20), nullable=False, server_default="link")  # 'link' or 'heading'
    slug = Column(String(200), nullable=True)  # optional if item_type is heading
    display_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    section = relationship("MenuHeaderSection", back_populates="items")
    translations = relationship("MenuHeaderItemTranslation", back_populates="item", cascade="all, delete-orphan")
    sub_items = relationship("MenuHeaderSubItem", back_populates="parent_item", cascade="all, delete-orphan")


class MenuHeaderItemTranslation(Base):
    __tablename__ = "menu_header_item_translations"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("menu_header_items.id", ondelete="CASCADE"), nullable=False)
    lang_code = Column(String(5), nullable=False)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), nullable=True)  # language-specific slug for URL

    item = relationship("MenuHeaderItem", back_populates="translations")


class MenuHeaderSubItem(Base):
    __tablename__ = "menu_header_sub_items"

    id = Column(Integer, primary_key=True, index=True)
    parent_item_id = Column(Integer, ForeignKey("menu_header_items.id", ondelete="CASCADE"), nullable=False)
    sub_item_type = Column(String(20), nullable=False, server_default="link")  # 'link' or 'heading'
    slug = Column(String(200), nullable=True)
    display_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    parent_item = relationship("MenuHeaderItem", back_populates="sub_items")
    translations = relationship("MenuHeaderSubItemTranslation", back_populates="sub_item", cascade="all, delete-orphan")
    sub_sub_items = relationship("MenuHeaderSubSubItem", back_populates="parent_sub_item", cascade="all, delete-orphan")


class MenuHeaderSubItemTranslation(Base):
    __tablename__ = "menu_header_sub_item_translations"

    id = Column(Integer, primary_key=True, index=True)
    sub_item_id = Column(Integer, ForeignKey("menu_header_sub_items.id", ondelete="CASCADE"), nullable=False)
    lang_code = Column(String(5), nullable=False)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), nullable=True)

    sub_item = relationship("MenuHeaderSubItem", back_populates="translations")


class MenuHeaderSubSubItem(Base):
    __tablename__ = "menu_header_sub_sub_items"

    id = Column(Integer, primary_key=True, index=True)
    parent_sub_item_id = Column(Integer, ForeignKey("menu_header_sub_items.id", ondelete="CASCADE"), nullable=False)
    slug = Column(String(200), nullable=False)
    display_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    parent_sub_item = relationship("MenuHeaderSubItem", back_populates="sub_sub_items")
    translations = relationship("MenuHeaderSubSubItemTranslation", back_populates="sub_sub_item", cascade="all, delete-orphan")


class MenuHeaderSubSubItemTranslation(Base):
    __tablename__ = "menu_header_sub_sub_item_translations"

    id = Column(Integer, primary_key=True, index=True)
    sub_sub_item_id = Column(Integer, ForeignKey("menu_header_sub_sub_items.id", ondelete="CASCADE"), nullable=False)
    lang_code = Column(String(5), nullable=False)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), nullable=False)

    sub_sub_item = relationship("MenuHeaderSubSubItem", back_populates="translations")