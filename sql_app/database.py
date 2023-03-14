from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib import parse
host = 'bj-cynosdbmysql-grp-6m11pba6.sql.tencentcdb.com'
port = '26045'
username = 'desci_test_user'
password = parse.quote_plus('DeSci@21cm_testdb')
db = 'desci_testdb'
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(
    username=username, password=password, host=host, port=port, db=db)
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
#
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=3600, echo=True)
# conn = engine.connect()
# result = conn.execute('select 1 from user_info limit 10')
# print(result.fetchone())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
