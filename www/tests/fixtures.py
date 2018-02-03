

import pytest

from ncms import NCMS


@pytest.fixture()
def app():
    return NCMS()

