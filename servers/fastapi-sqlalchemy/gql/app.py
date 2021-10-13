from strawberry import Schema
from strawberry.asgi import GraphQL

from gql.schema import Root

graphql_app = GraphQL(schema=Schema(Root))
