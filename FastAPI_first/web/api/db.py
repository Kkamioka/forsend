from sqlarchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlarchemy.orm import sessionmaker, declarative_base

ASYNC_DB_URL = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
      'user': "my",
      'password': "my",
      'host': "FirstAPI_db_1",
      'db_name': "my"
  })
  
async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
    
BASE = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session
 


