from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib import parse
SQLALCHEMY_DATABASE_URL = "sqlite:///{db}.db".format(db='desci')

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=3600, echo=True)
# conn = engine.connect()
# result = conn.execute('select 1 from user_info limit 10')
# print(result.fetchone())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
