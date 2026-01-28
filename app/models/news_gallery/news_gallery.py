from app.core.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func, Boolean

class NewsGallery(Base):
    __tablename__ = "news_gallery"

    id = Column(Integer, primary_key=True, index=True)
    news_id = Column(Integer, nullable=False)
    image = Column(Text, nullable=False)
    is_cover = Column(Boolean, nullable=False)