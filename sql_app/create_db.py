from database import  Base, engine
from models import User, Journal, Follow, Admin, Article


Base.metadata.create_all(engine)