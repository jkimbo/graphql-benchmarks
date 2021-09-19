import graphene


from movies.models import get_all_movies


class Director(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()

    @classmethod
    def from_instance(cls, instance):
        return cls(
            id=instance.id,
            name=instance.name,
        )


class Movie(graphene.ObjectType):
    id = graphene.Int()
    imdb_id = graphene.String()
    title = graphene.String()
    year = graphene.Int()
    image_url = graphene.String()
    imdb_rating = graphene.Float()
    imdb_rating_count = graphene.String()

    director = graphene.Field(Director)

    _instance = None

    def __init__(self, _instance, **kwargs):
        self._instance = _instance
        return super().__init__(**kwargs)

    def resolve_director(self, info):
        return Director.from_instance(self._instance.director)

    @classmethod
    def from_instance(cls, instance):
        return cls(
            _instance=instance,
            id=instance.id,
            imdb_id=instance.imdb_id,
            title=instance.title,
            year=instance.year,
            image_url=instance.image_url,
            imdb_rating=instance.imdb_rating,
            imdb_rating_count=instance.imdb_rating_count,
        )


class Query(graphene.ObjectType):
    top_250 = graphene.List(Movie)

    def resolve_top_250(self, info):
        movies = get_all_movies()
        return [Movie.from_instance(movie) for movie in movies]


schema = graphene.Schema(Query)
