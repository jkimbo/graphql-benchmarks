from django.contrib import admin
from django.urls import path, include

from strawberry.django.views import AsyncGraphQLView

from api.schema import schema


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "graphql/",
        AsyncGraphQLView.as_view(schema=schema, graphiql=True),
    ),
]
