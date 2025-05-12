import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL

@strawberry.type
class User:
    id: int
    name: str

@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: int) -> User:
        return User(id=id, name="John Doe")

@strawberry.type
class Mutation:
    @strawberry.mutation
    def update_user_name(self, id: int, name: str) -> User:
        return User(id=id, name=name)

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQL(schema)

app = FastAPI()
app.add_route("/graphql", graphql_app)
