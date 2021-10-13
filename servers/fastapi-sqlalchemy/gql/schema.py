from typing import List

import strawberry
from sqlalchemy import select
from sqlalchemy.orm import selectinload, relationship

from db import queries
from db.base import get_session
from db.models import Movie


@strawberry.type(name="Director")
class DirectorType:
    id: int
    name: str


@strawberry.type(name="Movie")
class MovieType:
    id: int
    imdb_id: str
    title: str
    year: int
    image_url: str
    imdb_rating: float
    imdb_rating_count: str

    director: DirectorType


@strawberry.type
class Root:
    @strawberry.field
    async def top_250(self) -> List[MovieType]:
        return await queries.get_all_movies()
