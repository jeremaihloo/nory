import asyncio
import pytest
import importlib

from camel_case_switcher import CamelCaseToUnderscope
from info_generators import NameGenerator
from dbs import BaseModel
import random


def generator_name(name_lenth: (4, 8)):
    letters = 'abcdefghijklmnopqrstuvwkyz'
    name = []
    for item in range(name_lenth[0], name_lenth[1]):
        index = random.randint(0, len(letters))
        name.append(letters[index])
    return name


def get_model_underscore_names():
    m = importlib.import_module('models')
    m_s = [x for x in dir(m) if issubclass(getattr(m, x), BaseModel)]
    return [CamelCaseToUnderscope(x) for x in m_s]


def mock_model_entry(model_name):
    entry = {
        'name': generator_name(),
        'title': NameGenerator.get(),
        'description': NameGenerator.get()
    }
    if model_name == 'menu':
        entry['target'] = generator_name()
    if model_name == 'permission':
        entry['type'] = generator_name()
    return entry


def mock_model_mapping(left, right):
    mapping = {
        left:generator_name()
    }


def check_response_data(res):
    pass


@pytest.mark.asyncio
async def test_apis():
    await asyncio.sleep(2)


@pytest.mark.asyncio
async def test_2():
    await asyncio.sleep(2)
