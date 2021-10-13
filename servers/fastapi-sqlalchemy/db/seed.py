import asyncio

import json

from db.base import get_session
from db.models import Director, Movie


async def main():
    with open("movies.json") as file:
        data = json.load(file)

    directors = []
    for movie in data:
        directors.append(Director(name=movie["director"]["name"]))

    async with get_session() as session:
        for movie in data:
            movie_model = Movie(
                imdb_id=movie["imdb_id"],
                imdb_rating=movie["imdb_rating"],
                title=movie["title"],
                year=movie["year"],
                image_url=movie["image_url"],
                imdb_rating_count=movie["imdb_rating_count"],
                director=next(director for director in directors if director.name == movie["director"]["name"])
            )
            session.add(movie_model)
        await session.commit()

if __name__ == '__main__':
    asyncio.run(main())
