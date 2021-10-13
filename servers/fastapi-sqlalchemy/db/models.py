from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base


class Director(Base):
    __tablename__ = "directors"
    id = Column(Integer(), primary_key=True)

    name = Column(String(40), nullable=False)


class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer(), primary_key=True)

    imdb_id = Column(String(40), nullable=False)
    title = Column(String(120), nullable=False)
    year = Column(Integer(), nullable=False)
    image_url = Column(String(255), nullable=False)
    imdb_rating = Column(Float(), nullable=False)
    imdb_rating_count = Column(String(40), nullable=False)

    director_id = Column(
        Integer(),
        ForeignKey("directors.id"),
        nullable=False,
    )
    director = relationship(Director)
