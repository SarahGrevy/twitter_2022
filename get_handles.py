from sqlalchemy import and_
from sqlalchemy import Integer, Column, String, Time
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Twitter_Handle(Base):

    __tablename__ = 'twitter_handle'


    id = Column(Integer, primary_key=True)
    twitter_handle = Column(String)
    # newsroom = Column(String)
    list_id = Column(String)
    followers_count = Column(Integer)
    user_created_date= Column(Time)
    bio = Column(String)
    location = Column(String)
    verified = Column(String)


    def __init__(self, **kwargs):
        self.twitter_handle = kwargs.get('twitter_handle')
        # self.newsroom = kwargs.get('newsroom')
        self.list_id = kwargs.get('list_id')
        self.followers_count = kwargs.get('followers_count')
        self.user_created_date = kwargs.get('user_created_date')
        self.bio = kwargs.get('bio')
        self.location = kwargs.get('location')
        self.verified = kwargs.get('verified')


       

    def upsert(self, dba, update_existing=True):
        with dba.session_scope() as session:
            rs = session.query(Twitter_Handle).filter(and_(
                Twitter_Handle.twitter_handle == self.twitter_handle
            ))
            exists = session.query(rs.exists()).scalar()
            if not exists:
                session.add(self)
                session.flush()
            elif update_existing:
                rs.update(self.keywords)
                session.flush()

    def insert(self, dba):
        self.upsert(dba, False)


      