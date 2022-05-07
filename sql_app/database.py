from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer, Boolean
from config import db_credentials
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = f'postgresql://{db_credentials["user"]}:{db_credentials["password"]}@{db_credentials["host"]}/{db_credentials["database"]}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

class Dictionary(Base):
    __tablename__ = 'dictionary'
    word = Column(String, primary_key=True, index=True)
    sorted_letters = Column(String, nullable=False)
    word_len = Column(Integer, nullable=False)
    is_noun = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"<Dictionary(word:{self.word}, sorted_letters: {self.sorted_letters}, word_len: {self.word_len})"

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
