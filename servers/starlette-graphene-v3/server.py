from starlette.applications import Starlette
from starlette.routing import Route
from starlette.graphql import GraphQLApp
import graphene


class TestObject(graphene.ObjectType):
    string = graphene.String()


class Query(graphene.ObjectType):
    string = graphene.String()
    list_of_strings = graphene.List(graphene.String)
    list_of_objects = graphene.List(TestObject)

    def resolve_string(self, info):
        return "Hello World!"

    def resolve_list_of_strings(self, info):
        return ["Hello World!"] * 100

    def resolve_list_of_objects(self, info):
        return [ TestObject(string="Hello World!") ] * 100


schema = graphene.Schema(query=Query)

routes = [
    Route('/graphql/', GraphQLApp(schema=schema))
]

app = Starlette(routes=routes)