import json

from graphql import (
    graphql, GraphQLSchema, GraphQLObjectType, GraphQLField, GraphQLString, GraphQLList, format_error
)

TestObject = GraphQLObjectType(
    name="TestObject",
    fields={
        "string": GraphQLField(
            GraphQLString,
            resolve=lambda obj, info: obj['string']
        )
    }
)

schema = GraphQLSchema(
    query=GraphQLObjectType(
        name='Query',
        fields={
            'string': GraphQLField(
                GraphQLString,
                resolve=lambda obj, info: 'Hello World!'
            ),
            'listOfStrings': GraphQLField(
                GraphQLList(GraphQLString),
                resolve=lambda obj, info: ["Hello World!"] * 100
            ),
            'listOfObjects': GraphQLField(
                GraphQLList(TestObject),
                resolve=lambda obj, info: [ { "string": "Hello World!" } ] * 100
            ),
        }
    )
)

async def app(scope, receive, send):
    if scope['type'] == "http" and scope['path'] == '/graphql/' and scope["method"] == "POST":
        request = await receive()

        data = json.loads(request['body'].decode())

        try:
            query = data["query"]
            variables = data.get("variables")
            operation_name = data.get("operationName")
        except KeyError:
            await send({
                "type": "http.response.start",
                "status": 400
            })
            await send({
                "type": "http.response.body",
                "body": "No GraphQL query found in the request".encode()
            })
        
        result = await graphql(
            schema, query, variable_values=variables, operation_name=operation_name
        )

        response_data = {"data": result.data}

        if result.errors:
            response_data["errors"] = [format_error(err) for err in result.errors]

        await send({
            "type": "http.response.start",
            "status": 200
        })
        await send({
            "type": "http.response.body",
            "body": json.dumps(response_data).encode()
        })

    else:
        await send({
            "type": "http.response.start",
            "status": 404
        })
        await send({
            "type": "http.response.body",
            "body": "URL not found".encode()
        })