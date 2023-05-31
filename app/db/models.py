from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date
from db import Base

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
