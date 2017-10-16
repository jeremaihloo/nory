import asyncio
import models
from migrations import MigrationBuilder


def create_builder():
    builder = MigrationBuilder(1, 'init')
    builder.add_tables([
        models.ContentType,
        models.ContentField,
        models.ContentModel,
        models.ContentModelField,
        models.Content,
        models.ContentItem,
        models.User
    ])
    return builder
