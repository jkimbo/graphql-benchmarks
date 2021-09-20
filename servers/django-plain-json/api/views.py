from django.http import JsonResponse

from movies.models import get_all_movies


def top_250(request):
    data = []
    movies = get_all_movies()
    for movie in movies:
        data.append(
            {
                "id": movie.id,
                "title": movie.title,
                "year": movie.year,
                "image_url": movie.image_url,
                "imdb_rating": movie.imdb_rating,
                "imdb_rating_count": movie.imdb_rating_count,
                "director": {
                    "id": movie.director.id,
                    "name": movie.director.name,
                },
            }
        )

    return JsonResponse(data, safe=False)
