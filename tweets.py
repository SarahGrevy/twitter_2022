from sqlalchemy import and_
from sqlalchemy import Integer, Column, String, Time
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tweets(Base):

    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    tweet = Column(String)
    date_created = Column(Time)
    followers_count = Column(String)

    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.tweet = kwargs.get('tweet')
        self.date_created = kwargs.get('date_created')
        self.followers_count = kwargs.get('followers_count')

    def upsert(self, dba, update_existing=True):
        with dba.session_scope() as session:
            rs = session.query(Tweets).filter(and_(
                Tweets.tweet == self.tweet
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


      