
import models
from migrations import MigrationBuilder

def create_builder():
    builder = MigrationBuilder(2, 'add_content_type')
    builder.add_tables([models.ContentType])
    return builder