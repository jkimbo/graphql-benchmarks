from fastapi import APIRouter

from db import queries
from . import schema

api_router = APIRouter()


@api_router.get(
    "/movies",
    response_model=list[schema.MovieSchema],
)
async def get_movies():
    return await queries.get_all_movies()
