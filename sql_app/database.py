from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib import parse
# host = '127.0.0.1'
# port = '3306'
# username = 'root'
# password = parse.quote_plus('DeSci@21cm_testdb')
db = 'test'
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(
#     username=username, password=password, host=host, port=port, db=db)
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = 'sqlite:///{db}.db'.format(db=db)
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=3600, echo=True)
# conn = engine.connect()
# result = conn.execute('select 1 from user_info limit 10')
# print(result.fetchone())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
