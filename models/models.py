from sqlalchemy import create_engine,Column,String,Integer,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from bson import  ObjectId
import time

from configs import config

engine = create_engine(config.DB_CONNECT, echo=False)
Sess = sessionmaker(bind=engine)
DB = Sess()
BaseModel = declarative_base()


class Api(BaseModel):
    __tablename__ = 'api'
    id = Column(String(64),primary_key=True)#api的唯一id
    route = Column(String(20),default='')#api地址

class Authority(BaseModel):
    __tablename__='authority'
    user_id=Column(String(64),primary_key=True)
    api_id=Column(String(64))
    count=Column(Integer,default=0)#剩余调用数量

class User(BaseModel):
    __tablename__='user'
    id=Column(String(64),primary_key=True)
    password=Column(String(64))

class Key(BaseModel):
    __tablename__='key'
    key=Column(String(64),primary_key=True)
    user_id=Column(String(64))
    secret = Column(String(64))

if __name__=='__main__':
    BaseModel.metadata.create_all(engine)