from infrastructures.cli import run_command
import pytest

@pytest.mark.asyncio
async def test_cmd():
    r = await run_command('configs db_host --debug=False')
    assert r is True