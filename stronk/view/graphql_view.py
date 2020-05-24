from flask_graphql import GraphQLView as BaseGraphQLView
from graphql.error.format_error import format_error


class CustomGraphQLView(BaseGraphQLView):

    @staticmethod
    def format_error(error):
        """Extend base error formatter to include a context."""
        formatted_error = format_error(error)

        try:
            formatted_error['context'] = error.original_error.context
        except AttributeError:
            pass

        return formatted_error
