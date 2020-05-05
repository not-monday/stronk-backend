from snapshottest import TestCase
from graphene.test import Client

from stronk import db
from stronk.schema import schema
from tests.helpers import get_test_db_session


class TestQuery(TestCase):
    # TODO: Update tests to use testing data.
    def setUp(self):
        self.session = get_test_db_session()
        self.client = Client(schema)

    def test_query_all_fields(self):
        query = '''
                {
                    users {
                        id
                        name
                        username
                        email
                        currentProgram
                    }
                }
                '''
        self.assertMatchSnapshot(self.client.execute(
            query, context_value={'session': self.session}))

    def test_query_user_by_id(self):
        query = '''
                {
                    user(id:"test1") {
                        id
                        name
                        username
                        email
                        currentProgram
                    }
                }
                '''
        self.assertMatchSnapshot(self.client.execute(
            query, context_value={'session': self.session}))
