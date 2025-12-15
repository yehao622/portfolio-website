"""
Database setup and models for visitor tracking.
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.config.settings import settings

# Create database engine
engine = create_engine(settings.database_url, echo=settings.debug)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


class Visitor(Base):
    """Visitor tracking model."""
    __tablename__ = "visitors"
    
    id = Column(Integer, primary_key=True, index=True)
    visit_date = Column(DateTime, default=datetime.now, nullable=False)
    ip_hash = Column(String(64), nullable=True)
    user_agent = Column(Text, nullable=True)
    page_visited = Column(String(255), nullable=False)


class ChatSession(Base):
    """Chat session tracking model (optional for Phase 2)."""
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(36), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    messages_count = Column(Integer, default=0)


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for getting database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()