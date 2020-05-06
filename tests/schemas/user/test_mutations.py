from unittest.mock import patch

from graphene.test import Client
from snapshottest import TestCase

from stronk.models.program import Program
from stronk.models.user import User
from stronk.schema import schema
from tests import helpers as h


@patch("stronk.models.user.db.session")
@patch("stronk.schemas.user.mutations.g")
@patch("stronk.schemas.user.mutations.auth.get_user")
class TestCreateUser(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = h.get_test_db_session()
        super().setUpClass()

    def setUp(self):
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

    def test_create_user_without_current_program(self, mock_get_user, mock_g, mock_db_session):
        mock_db_session = self.session
        mock_get_user.return_value = "test_id"
        query = '''
            mutation {
                createUser(email: "test_email", username: "test_username", name: "test_name") {
                    user {
                        id
                        name
                        username
                        email
                        currentProgram
                    }
                }
            }
        '''
        self.assertMatchSnapshot(self.client.execute(
            query, context_value={'session': self.session}))

    def test_create_user_with_current_program(self, mock_get_user, mock_g, mock_db_session):
        mock_db_session = self.session
        mock_get_user.return_value = "test_id"
        query = '''
            mutation {
                createUser(email: "test_email", username: "test_username", name: "test_name", currentProgram: 0) {
                    user {
                        id
                        name
                        username
                        email
                        currentProgram
                    }
                }
            }
        '''
        # Custom set up
        h.execute(self.session, "mock/insert_users.sql")
        h.execute(self.session, "mock/insert_programs.sql")

        result = self.client.execute(
            query, context_value={'session': self.session})

        # Custom tear down
        self.session.query(Program).delete()
        self.assertMatchSnapshot(result)
