from playhouse.shortcuts import model_to_dict

from infrastructures.dbs import objects
import math


class Pagination(dict):
    def __init__(self, page_total, page_index, page_size=20, items=None):
        self.page_total = page_total
        self.page_index = page_index
        self.page_size = page_size
        self.items = [] if items is None else items

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, item):
        return self[item]

async def get_pagination(query, page_index, page_size=20):
    count = await objects.count(query)
    page_total = math.ceil(count / page_size)
    items = await objects.execute(query.paginate(page_index, page_size))
    return Pagination(
        page_total=page_total,
        page_index=page_index,
        page_size=page_size,
        items=[model_to_dict(x) for x in items]
    )
