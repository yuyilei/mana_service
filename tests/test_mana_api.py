import os
import json
import base64
from aiohttp.test_utils import TestClient, loop_context

def test_mana_api(app):
    with loop_context() as loop:
        with TestClient(app, loop=loop) as client:

            async def get_auth_header():
                admin = os.getenv('ADMIN')
                adminpwd = os.getenv('ADMINPWD')
                auth_header = {'Authorization': 'Basic %s' % (base64.b64encode(admin.encode()+
                    b':'+adminpwd.encode())).decode()}
                return auth_header

            async def _test_apartment_api():
                nonlocal client
                resp = await client.get('/api/apartment/')
                assert resp.status == 200
                print('... test apartment api [OK]')

            async def _test_banner_post_api():
                nonlocal client
                auth_header = await get_auth_header()
                post_data = {
                        'img': 'https://y.gtimg.cn/music/photo_new/T002R300x300M000001Fk5RB3SErqf.jpg',
                        'url': 'https://muxixyz.com',
                        'num': '1'
                }
                resp = await client.post('/api/ios/banner/', data=json.dumps(post_data), headers=auth_header)
                assert resp.status == 201
                print('... test banner post api [OK]')

            async def _test_banner_update_api():
                nonlocal client
                auth_header = await get_auth_header()
                post_data = {
                        'img': 'https://y.gtimg.cn/music/photo_new/T002R300x300M000001Fk5RB3SErqf.jpg',
                        'num': '2'
                }
                resp = await client.put('/api/ios/banner/', data=json.dumps(post_data), headers=auth_header)
                assert resp.status == 200
                print('... test banner update api [OK]')

            async def _test_banner_get_api():
                nonlocal client
                resp = await client.get('/api/ios/banner/')
                assert resp.status == 200
                print('... test banner get api [OK]')

            async def _test_banner_del_api():
                nonlocal client
                auth_header = await get_auth_header()
                resp = await client.delete('/api/ios/banner/?name=%s' % \
                        'https://y.gtimg.cn/music/photo_new/T002R300x300M000001Fk5RB3SErqf.jpg',
                        headers=auth_header)
                assert resp.status == 200
                print('... test banner del api [OK]')

            async def _test_product_put_api():
                nonlocal client
                auth_header = await get_auth_header()
                post_data = {
                        'name': '学而', 'icon': 'xxx',
                        'url': 'https://xueer.muxixyz.com', 'intro': '学而'
                }
                resp = await client.put('/api/product/', data=json.dumps(post_data), headers=auth_header)
                assert resp.status == 200
                print('... test product del api [OK]')

            async def _test_product_get_api():
                nonlocal client
                resp = await client.get('/api/product/')
                assert resp.status == 200
                print('... test product get api [OK]')

            async def _test_product_del_api():
                nonlocal client
                auth_header = await get_auth_header()
                resp = await client.delete('/api/product/?name=%s' % '学而', headers=auth_header)
                assert resp.status == 200
                print('... test product del api [OK]')

            async def _test_calendar_update_api():
                nonlocal client
                auth_header = await get_auth_header()
                post_data = { 'img': 'xxxxx', 'size': '133x144' }
                resp = await client.post('/api/calendar/', headers=auth_header, data=json.dumps(post_data))
                assert resp.status == 201
                print('... test calendar update api [OK]')

            async def _test_calendar_get_api():
                nonlocal client
                resp = await client.get('/api/calendar/')
                assert resp.status == 200
                print('... test calenar get api [OK]')

            async def _test_start_update_api():
                nonlocal client
                auth_header = await get_auth_header()
                post_data = { 'img': 'xxxxx', 'url': 'http://xxxx.xxx' }
                resp = await client.post('/api/start/', headers=auth_header, data=json.dumps(post_data))
                assert resp.status == 201
                print('... test start update api [OK]')

            async def _test_start_get_api():
                nonlocal client
                resp = await client.get('/api/start/')
                assert resp.status == 200
                print('... test start get api [OK]')

            loop.run_until_complete(_test_apartment_api())
            loop.run_until_complete(_test_banner_post_api())
            loop.run_until_complete(_test_banner_update_api())
            loop.run_until_complete(_test_banner_get_api())
            loop.run_until_complete(_test_banner_del_api())
            loop.run_until_complete(_test_product_put_api())
            loop.run_until_complete(_test_product_get_api())
            loop.run_until_complete(_test_product_del_api())
            loop.run_until_complete(_test_calendar_update_api())
            loop.run_until_complete(_test_calendar_get_api())
            loop.run_until_complete(_test_start_update_api())
            loop.run_until_complete(_test_start_get_api())
