from sqlalchemy import create_engine,Column,String,Integer,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from configs import config

engine = create_engine(config.DB_CONNECT, echo=False)
Sess = sessionmaker(bind=engine)
DB = Sess()
BaseModel = declarative_base()


class Api(BaseModel):
    __tablename__ = 'apis'
    id = Column(String(64),primary_key=True)#api的唯一id
    route = Column(String(256),default='')#api地址

class Authority(BaseModel):
    __tablename__='authority'
    user_id=Column(String(64),primary_key=True)
    api_id=Column(String(64))
    count=Column(Integer,default=0)#剩余调用数量

class User(BaseModel):
    __tablename__='users'
    id=Column(String(64),primary_key=True)
    password=Column(String(64))

class Key(BaseModel):
    __tablename__='keys'
    keyid=Column(String(64),primary_key=True)
    user_id=Column(String(64))
    keysecret = Column(String(64))

if __name__=='__main__':
    # api=DB.query(Api).filter(Api.id=='/sms/sender/any_text_sender').first()
    # api.route='192.168.199.6:6678/sms/sender/any_text_sender'
    # api=Api(id='/sms/sender/any_text_sender',route='192.168.199.6:6678/sms/sender/any_text_sender')
    # DB.add(api)
    A=Authority(user_id='liangoy',api_id='/sms/sender/any_text_sender',count=str(10*8))
    DB.add(A)
    DB.commit()