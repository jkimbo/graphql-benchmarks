import logging
from aiohttp import web
from tartiflette import Resolver
from tartiflette_aiohttp import register_graphql_handlers

@Resolver("Query.string")
async def resolver_string(parent, args, ctx, info):
    return "Hello World!"

@Resolver("Query.listOfStrings")
async def resolver_list_of_strings(parent, args, ctx, info):
    return ["Hello World!"] * 100

@Resolver("Query.listOfObjects")
async def resolver_list_of_objects(parent, args, ctx, info):
    return [{ "string": "Hello World!" }] * 100

sdl = """
    type TestObject {
        string: String!
    }
    type Query {
        string: String!
        listOfStrings: [String!]!
        listOfObjects: [TestObject!]!
    }
"""

logging.basicConfig(level=logging.ERROR)


app = register_graphql_handlers(
    web.Application(),
    engine_sdl=sdl,
    executor_http_endpoint='/graphql/',
)