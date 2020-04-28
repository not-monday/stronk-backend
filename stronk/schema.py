from graphene import ObjectType, String, Schema

class Query(ObjectType):
    # defines query schema
    user = String(name=String(default_value="test user name"))
    workout = String(id=String(default_value="test workout id"))

    # TODO actual resolvers - these are just for show
    # resolvers
    def resolve_user(root, info, name):
        return f"user : {name}"

    def resolve_workout(root, info, id):
        return f"workout id : {id}"


schema = Schema(query=Query)