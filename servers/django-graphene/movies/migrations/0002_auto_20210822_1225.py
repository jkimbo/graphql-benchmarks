# Generated by Django 3.2.6 on 2021-08-22 12:25

import json
from django.db import migrations

from main.settings import BASE_DIR


def populate_data(apps, schema_editor):
    Movie = apps.get_model("movies", "Movie")
    Director = apps.get_model("movies", "Director")

    with open(BASE_DIR.parent.parent / "data/movies.json") as json_file:
        json_data = json.load(json_file)

    for movie in json_data:
        director, _ = Director.objects.get_or_create(name=movie["director"]["name"])
        Movie.objects.create(
            imdb_id=movie["imdb_id"],
            title=movie["title"],
            year=movie["year"],
            image_url=movie["image_url"],
            imdb_rating=movie["imdb_rating"],
            imdb_rating_count=movie["imdb_rating_count"],
            director=director,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0001_initial"),
    ]

    operations = [migrations.RunPython(populate_data, migrations.RunPython.noop)]
