from rest_framework import serializers, viewsets

from movies.models import Movie, Director, get_all_movies


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            "id",
            "imdb_id",
            "title",
            "year",
            "image_url",
            "imdb_rating",
            "imdb_rating_count",
            "director",
        ]
        depth = 1


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = [
            "id",
            "name",
        ]


class MovieViewSet(viewsets.ModelViewSet):
    queryset = get_all_movies()
    serializer_class = MovieSerializer
