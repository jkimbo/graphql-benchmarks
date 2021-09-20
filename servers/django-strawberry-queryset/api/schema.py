from typing import List
import strawberry

from movies.models import Movie as MovieModel, get_all_movies


@strawberry.type
class Director:
    id: int
    name: str

    @classmethod
    def from_instance(cls, instance):
        return cls(
            id=instance.id,
            name=instance.name,
        )


@strawberry.type
class Movie:
    id: int
    imdb_id: str
    title: str
    year: int
    image_url: str
    imdb_rating: float
    imdb_rating_count: str

    instance: strawberry.Private[MovieModel]

    @strawberry.field
    def director(self) -> Director:
        return self.director

    @classmethod
    def from_instance(cls, instance):
        return cls(
            instance=instance,
            id=instance.id,
            imdb_id=instance.imdb_id,
            title=instance.title,
            year=instance.year,
            image_url=instance.image_url,
            imdb_rating=instance.imdb_rating,
            imdb_rating_count=instance.imdb_rating_count,
        )


@strawberry.type
class Query:
    @strawberry.field
    def top_250(self) -> List[Movie]:
        return get_all_movies()


schema = strawberry.Schema(Query)
