from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

database_url = "" #setar como variavel de ambiente

engine = create_engine(database_url)

Base = declarative_base()

def get_db_session():
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    try:
        yield session
    except Exception as error:
        print(error)
    finally:
        session.close()