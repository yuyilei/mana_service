from . import create_app
from aiohttp.test_utils import TestClient, loop_context

def test_apartment_api(app):
    with loop_context() as loop:
        with TestClient(app, loop=loop) as client:

            async def _test_apartment_api():
                nonlocal client
                resp = await client.get('/api/apartment/')
                assert resp.status == 200

            loop.run_until_complete(_test_apartment_api())
