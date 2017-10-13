import unittest

import asyncio
from pprint import pprint

from config import configs
from migrations import MigrationBuilder
import models
import orm

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.builder = MigrationBuilder(1, 'init')

    def test_build(self):
        self.builder.add_tables([models.ContentModel, models.Content, models.ContentField, models.User])
        print(self.builder.lines[0]['sqls'])

    def test_drop(self):
        self.builder.drop_tables([models.ContentModel, models.ContentField, models.Content, models.User])
        print(self.builder.lines[0]['sqls'])
