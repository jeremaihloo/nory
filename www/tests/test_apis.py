import unittest

import pytest

import handlers

class MyTestCase(unittest.TestCase):

    @pytest.mark.asyncio
    async def test_create_content_type(self):
        content_type = await handlers.api_create_content_type(name='name', title='Name')
        assert content_type is not None
        print(content_type)

    # def test_create_field(self):
    #     self.assertEqual(True, False)
    #
    # def test_create_model(self):
    #     self.assertEqual(True, False)
    #
    # def test_create_content(self):
    #     self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
