from graphene import ObjectType, String, Schema

# from stronk.utils.auth import verify_token
# from functools import wraps

# def requires_auth(f):
#     @wraps
#     def wrapper():
#         # check the authenticity of the token
#         # TODO implement a more granular permissions scheme
#         verify_token
#     return wrapper


class Query(ObjectType):
    # defines query schema
    user = String(name=String(default_value="test user name"))
    workout = String(id=String(default_value="test workout id"))

    # TODO add resolvers
    # resolvers
    def resolve_user(root, info, name):
        return f"user : {name}"

    def resolve_workout(root, info, id):
        return f"workout id : {id}"


schema = Schema(query=Query)
# # examples for testing
# query = "{user(name: 'test')}"
# result = schema.execute(query)