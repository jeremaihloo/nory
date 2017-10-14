import models
from migrations import MigrationBuilder


def create_builder():
    builder = MigrationBuilder(0, 'init')
    builder.drop_tables([models.Content, models.ContentField, models.User, models.ContentModel])
    return builder
