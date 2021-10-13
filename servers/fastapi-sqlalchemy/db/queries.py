from sqlalchemy import select
from db.models import Movie
from db.base import get_session
from sqlalchemy.orm import selectinload


async def get_all_movies():
    query = select(Movie).options(selectinload(Movie.director))
    async with get_session() as session:
        movies = await session.scalars(query)
    return movies.all()
