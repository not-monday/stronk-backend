# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCreateUser::test_create_user_without_current_program 1'] = {
    'data': {
        'createUser': {
            'user': {
                'currentProgram': None,
                'email': 'test_email',
                'id': 'test_id',
                'name': 'test_name',
                'username': 'test_username'
            }
        }
    }
}

snapshots['TestCreateUser::test_create_user_with_current_program 1'] = {
    'data': {
        'createUser': {
            'user': {
                'currentProgram': 0,
                'email': 'test_email',
                'id': 'test_id',
                'name': 'test_name',
                'username': 'test_username'
            }
        }
    }
}
