import datetime 
from database import Base
from sqlalchemy import Column,Integer,String,JSON,TIMESTAMP



class NewsTable(Base):
    __tablename__ = "web_scraper"

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    Important_details   = Column(JSON)
    created_at          = Column(TIMESTAMP, default=datetime.datetime.utcnow)

