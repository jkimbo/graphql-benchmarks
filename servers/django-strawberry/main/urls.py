from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from strawberry.django.views import GraphQLView

from api.schema import schema


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "graphql/",
        csrf_exempt(GraphQLView.as_view(schema=schema, graphiql=True)),
    ),
]
