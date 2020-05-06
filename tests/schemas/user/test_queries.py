from snapshottest import TestCase
from graphene.test import Client

from stronk.models.user import User
from stronk.schema import schema
from tests import helpers as h


class TestQuery(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = h.get_test_db_session()
        super().setUpClass()

    def setUp(self):
        h.execute(self.session, "mock/insert_users.sql")
        self.client = Client(schema)
        super().setUp()

    def tearDown(self):
        self.session.query(User).delete()
        self.session.commit()
        super().tearDown()

    @classmethod
    def tearDownClass(cls):
        h.close_session(cls.session)
        super().tearDownClass()

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
                    user(id:"user_id_1") {
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
