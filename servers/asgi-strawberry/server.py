import strawberry
from strawberry.asgi import GraphQL
from typing import List


@strawberry.type
class TestObject:
    string: str


@strawberry.type
class Query:

    @strawberry.field
    def string(self, info) -> str:
        return "Hello World!"

    @strawberry.field
    def list_of_strings(self, info) -> List[str]:
        return ["Hello World!"] * 100

    @strawberry.field
    def list_of_objects(self, info) -> List[TestObject]:
        return [ TestObject(string="Hello World!") ] * 100


schema = strawberry.Schema(query=Query)

app = GraphQL(schema=schema)