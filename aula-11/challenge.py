import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL

@strawberry.type
class User:
    id: int
    name: str
    email: str

@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: int) -> User:
        return User(id=id, name="John Doe", email="john.doe@example.com")

@strawberry.type
class Mutation:
    @strawberry.mutation
    def update_user(self, id: int, name: str, email: str) -> User:
        return User(id=id, name=name, email=email)

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQL(schema)

app = FastAPI()
app.add_route("/graphql", graphql_app)


