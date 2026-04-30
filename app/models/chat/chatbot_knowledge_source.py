from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class ChatbotKnowledgeSource(Base):
    __tablename__ = "chatbot_knowledge_sources"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(Text, nullable=False, unique=True)
    label = Column(String(255), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    last_scraped_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    knowledge = relationship("ChatbotKnowledge", back_populates="source", cascade="all, delete-orphan")
