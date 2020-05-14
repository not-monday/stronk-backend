import os
import helpers as h

session = h.get_test_db_session()
try:
    # Load test data
    h.execute_from_file(session, "sql/insert_mock_data.sql")
    # Run Postman collection
    os.system("newman run postman/collection.json -e postman/env.json")
finally:
    # Clear all data from db
    h.execute_from_file(session, "sql/reset_tables.sql")
    h.close_session(session)
