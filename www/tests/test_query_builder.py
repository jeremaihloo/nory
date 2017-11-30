import unittest
import pytest

import norm
from apps.core.models import User, UserProfile


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

    def test_relation_query(self):
        q = (norm.Query().select(User)
                .include(User.profile)
                .where(User.name == 'lujiejie')
                .order_by_asc(User.created_at))
        print(q)
