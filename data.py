from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Messages(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    user_name = Column(String)
    telegram_id = Column(String)
    text = Column(String(1000), unique=True)
    time = Column(DateTime) 
    requested = Column(Boolean, default=False)
    
    
engine = create_engine("sqlite:///main.db")
Base.metadata.create_all(bind=engine)


class Database():
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()
    
    
    def add(self, title: str, user_name: str, telegram_id: str | int, text: str, time: datetime):
        message = Messages(title=title, user_name=user_name, telegram_id=telegram_id, text=text, time=time)
        
        try:
            self.session.add(message)
            self.session.commit()
        except: 
            pass
        
    
    def get_any(self):
        return self.session.query(Messages).all()
    
    
    def get_only_new(self):
        return self.session.query(Messages).filter(Messages.requested == False).all()
    
    
    def get_by_date(self, date: datetime):
        return self.session.query(Messages).filter(Messages.time.date() == date.date()).all()
    
    
    def close_session(self):
        self.session.close()



