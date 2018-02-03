from infrastructures.utils import singleton


@singleton
class TestModel(object):
    def __init__(self):
        self.value = 1001


def test_singleton():
    a = TestModel()
    b = TestModel()
    assert a == b
    a.value = 2
    assert b.value == 2
