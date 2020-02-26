from starlette.applications import Starlette
from starlette.routing import Route
from starlette.graphql import GraphQLApp
from ariadne import QueryType, make_executable_schema
from ariadne.asgi import GraphQL

type_defs = """
    type TestObject {
        string: String!
    }
    type Query {
        string: String!
        listOfStrings: [String!]!
        listOfObjects: [TestObject!]!
    }
"""

query = QueryType()

@query.field("string")
def resolve_string(*_):
    return "Hello World!"

@query.field("listOfStrings")
def resolve_list_of_strings(*_):
    return ["Hello World!"] * 100

@query.field("listOfObjects")
def resolve_list_of_objects(*_):
    return [{ "string": "Hello World!"}] * 100

schema = make_executable_schema(type_defs, query)

routes = [
    Route('/graphql/', GraphQL(schema=schema))
]

app = Starlette(routes=routes)