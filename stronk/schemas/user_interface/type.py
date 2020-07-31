import graphene


class UserInterface(graphene.Interface):
    name = graphene.String(required=True)
    username = graphene.String(required=True)
