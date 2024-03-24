from sqlalchemy import create_engine, update, Column, Integer, String, DateTime, Boolean
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
    
    
    def add(self, title: str, user_name: str = None, telegram_id: str | int = None, text: str = None, time: datetime = None):
        message = Messages(title=title, user_name=user_name, telegram_id=telegram_id, text=text, time=time)
        
        try:
            self.session.add(message)
            self.session.commit()
        except: 
            pass
        
    
    def get_any(self):
        messages = self.session.query(Messages).all()
        for i, message in enumerate(messages):
            self.session.execute(update(Messages).values(requested=True).where(Messages.id==message.id))
            m = messages[i].__dict__ 
            m.pop("_sa_instance_state")
            messages[i] = m
        
        return messages
    
    
    def get_by_date(self, date: datetime):
        messages = self.session.query(Messages).filter(Messages.time == date).all()
    
        for i, message in enumerate(messages):
            self.session.execute(update(Messages).values(requested=True).where(Messages.id==message.id))
            m = messages[i].__dict__ 
            m.pop("_sa_instance_state")
            messages[i] = m
        
        return messages
    
    
    def close_session(self):
        self.session.close()



