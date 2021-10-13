from fastapi import FastAPI

from gql.app import graphql_app
from rest.router import api_router

app = FastAPI()

app.mount("/graphql", graphql_app)
app.include_router(api_router)
