from sql_app.database import Base, engine
from sql_app.models import User, Journal, Follow, Admin, Article

Base.metadata.create_all(engine)
