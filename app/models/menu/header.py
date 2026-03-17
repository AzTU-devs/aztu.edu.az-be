from app.core.database import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey


class MenuHeaderSection(Base):
    __tablename__ = "menu_header_sections"

    id = Column(Integer, primary_key=True, index=True)
    section_key = Column(String(50), unique=True, nullable=False)
    image_url = Column(Text, nullable=False)
    direct_url = Column(Text, nullable=True)
    display_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)


class MenuHeaderSectionTranslation(Base):
    __tablename__ = "menu_header_section_translations"

    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("menu_header_sections.id", ondelete="CASCADE"), nullable=False)
    lang_code = Column(String(5), nullable=False)
    label = Column(String(100), nullable=False)
    base_path = Column(String(200), nullable=False)


class MenuHeaderItem(Base):
    __tablename__ = "menu_header_items"

    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("menu_header_sections.id", ondelete="CASCADE"), nullable=False)
    item_type = Column(String(20), nullable=False, server_default="link")  # 'link' | 'subheader'
    slug = Column(String(200), nullable=True)
    display_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)


class MenuHeaderItemTranslation(Base):
    __tablename__ = "menu_header_item_translations"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("menu_header_items.id", ondelete="CASCADE"), nullable=False)
    lang_code = Column(String(5), nullable=False)
    title = Column(String(200), nullable=False)


class MenuHeaderSubItem(Base):
    __tablename__ = "menu_header_sub_items"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("menu_header_items.id", ondelete="CASCADE"), nullable=False)
    slug = Column(String(200), nullable=False)
    display_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)


class MenuHeaderSubItemTranslation(Base):
    __tablename__ = "menu_header_sub_item_translations"

    id = Column(Integer, primary_key=True, index=True)
    sub_item_id = Column(Integer, ForeignKey("menu_header_sub_items.id", ondelete="CASCADE"), nullable=False)
    lang_code = Column(String(5), nullable=False)
    title = Column(String(200), nullable=False)
