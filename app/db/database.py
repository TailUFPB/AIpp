from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class App(Base):
    __tablename__ = "App"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    qtd_ratings = Column(Integer, default=0)
    qtd_reviews = Column(Integer, default=0)
    avg_score = Column(Float, default=0.0)


class Reviews(Base):
    __tablename__ = "Reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    review_text = Column(Text, nullable=False)
    score = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    time = Column(Date)
    year_time = Column(Integer)
    app_id = Column(Integer, ForeignKey("App.id"), nullable=False)

    app_fk = relationship("App", back_populates="Reviews", cascade="all, delete")

database_url = "" #setar como variavel de ambiente

engine = create_engine(database_url)

Base.metadata.create_all(bind=engine) #Cria database, se não existir

def get_db_session():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db_session = SessionLocal()
    try:
        yield db_session
    except Exception as error:
        print(error)
    finally:
        db_session.close()