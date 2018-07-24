import os

from nory.infras.exts.managers import ExtensionManager
from nory.infras.web.nweb import WebBuilder


def test_builder():
    builder  = WebBuilder('test', os.path.dirname(__file__))
    assert builder.ext_manager is None
    builder.use_ext_manager([__package__])
    assert isinstance(builder.ext_manager, ExtensionManager)
