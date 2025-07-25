from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "mysql+pymysql://essay_user:password123@localhost/essay_feedback"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Essay(Base):
    __tablename__ = "essays"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    author = Column(String(100), default="Anonymous")
    content_length = Column(Integer)
    feedback = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class FileModel(Base):
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), nullable=False)
    filename = Column(String(255), nullable=False)
    content_type = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()