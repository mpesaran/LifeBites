# from os import getenv
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker

# USER = 'hbnb'
# PWD = 'hbnb_password'
# HOST = 'localhost'
# DB = 'hbnb_db'

# Base = declarative_base()
# engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(USER, PWD, HOST, DB))
# Base.metadata.create_all(engine)

# session_factory = sessionmaker(bind=engine, expire_on_commit=False)

# session = scoped_session(session_factory)

