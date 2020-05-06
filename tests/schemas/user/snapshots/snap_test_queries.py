# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestQuery::test_query_all_fields 1'] = {
    'data': {
        'users': [
            {
                'currentProgram': None,
                'email': 'max.wavy@gmail.com',
                'id': 'user_id_1',
                'name': 'max b wavy',
                'username': 'mxwvy'
            },
            {
                'currentProgram': None,
                'email': 'ka.kit@gmail.com',
                'id': 'user_id_2',
                'name': 'jason cheung',
                'username': 'kakit'
            },
            {
                'currentProgram': None,
                'email': 'richard.wei@gmail.com',
                'id': 'user_id_3',
                'name': 'richard wei',
                'username': 'chengchu'
            }
        ]
    }
}

snapshots['TestQuery::test_query_user_by_id 1'] = {
    'data': {
        'user': {
            'currentProgram': None,
            'email': 'max.wavy@gmail.com',
            'id': 'user_id_1',
            'name': 'max b wavy',
            'username': 'mxwvy'
        }
    }
}
