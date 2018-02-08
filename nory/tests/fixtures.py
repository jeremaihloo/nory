

import pytest

from application import NCMS


@pytest.fixture()
def app():
    return NCMS()

