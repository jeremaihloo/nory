from apps.core import models
from migrations_core import Migration


class MigrationInit(Migration):
    def __init__(self):
        self.version = 1
        self.name = 'init'

        super(MigrationInit, self).__init__(version=self.version, name=self.name)

    def do(self):
        self.builder.add_tables([
            models.ContentType,
            models.ContentField,
            models.ContentModel,
            models.ContentModelField,
            models.Content,
            models.ContentItem,
            models.User
        ], force=True)

    def undo(self):
        self.builder.drop_tables([
            models.ContentType,
            models.ContentField,
            models.ContentModel,
            models.ContentModelField,
            models.Content,
            models.ContentItem,
            models.User
        ])
