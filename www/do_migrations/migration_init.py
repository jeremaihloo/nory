import asyncio
import models
from migrations import MigrationBuilder

def create_builder():
    builder = MigrationBuilder(1, 'init')
    builder.add_tables([models.ContentModel, models.Content, models.ContentField, models.User])
    return builder
