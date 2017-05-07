import os
import ast
import time
import aioredis
from aiohttp import web
from aiohttp.web import Response
from .decorator import require_admin_login

REDISHOST = os.getenv('REDISHOST') or 'redis1'
REDISPORT = int(os.getenv('REDISPORT') or '6384')

api = web.Application()

apartment_list = [
        {
            'apartment': "学生事务大厅",
            'phone': ["67865591"],
            'place': "文华公书林（老图书馆）3楼"
        },
        {
            'apartment': "校医院",
            'phone': ["67867176"],
            'place': "九号楼侧边下阶梯右转处"
        },
        {
            'apartment': "水电费缴纳处",
            'phone': ["67861701"],
            'place': "东南门附近的水电修建服务中心内"
        },
        {
            'apartment': "校园卡管理中心",
            'phone': ["67868524"],
            'place': "田家炳楼侧边阶梯旁"
        },
        {
            'apartment': "教务处",
            'phone': ["67868057"],
            'place': "行政楼2楼"
        },
        {
            'apartment': "学生资助中心",
            'phone': ["67867877"],
            'place': "学生事务大厅10号窗口"
        },
        # {
        #     'apartment': "校团委",
        #     'phone': ["67867539"],
        #     'place': "行政楼副楼301"
        # },
        {
            'apartment': "党校办公室",
            'phone': ["67868011"],
            'place': "行政楼副楼",
        },
        {
            'apartment': "素质教育办公室",
            'phone': ["67868057"],
            'place': "暂无",
        },
        {
            'apartment': "档案馆",
            'phone': ["67867198"],
            'place': "科学会堂一楼",
        },
        {
            'apartment': "国际交流事务办",
            'phone': ["67861299"],
            'place': "法学院前面的路口左拐（有路标）",
        },
        {
            'apartment': "心理咨询中心",
            'phone': ["67868274"],
            'place': "文华公书林（老图书馆）3楼",
        },
        {
            'apartment': "保卫处",
            'phone': ["67868110"],
            'place': "化学逸夫楼斜对面",
        },
]

async def apartment_info_api(request):
    return web.json_response(apartment_list)

async def product_get_api(request):
    """
    key: products
    value:
        {
            "_products": [{
                "name": "产品名称",
                "icon": "学而icon七牛外链",
                "url": "产品url",
                "intro": "产品介绍"
            },]
            "update": "1234.5"
        }
    """
    pool = await aioredis.create_pool(REDISHOST, REDISPORT)
    async with pool as redis:
        products = await redis.get('products') or '{}'
        products_dict = ast.literal_eval(products)
        return web.json_response(products_dict)

@require_admin_login
async def product_add_api(request):
    json_data = await request.json()
    pool = await aioredis.create_pool(REDISHOST, REDISPORT)
    async with pool as redis:
        products = await redis.get('products') or '{}'
        products_dict = ast.literal_eval(products)
        products_dict['_products'].append(json_data)
        products_dict['update'] = time.time()
        await redis.set('products', products_dict)
        return web.json_response({})

@require_admin_login
async def product_del_api(request):
    product = await request.rel_url.query['name']
    pool = await aioredis.create_pool(REDISHOST, REDISPORT)
    async with pool as redis:
        products = await redis.get('products') or '{}'
        products_dict = ast.literal_eval(products)
        products_list = products_dict['_products']
        for p in products_list:
            if p.get('name') == product:
                products_list.remove(p)
                products_dict['_products'] = products_list
                products_dict['update'] = time.time()
                await redis.set('products', products_dict)
                return web.json_response({})
            return web.Response(b'{}', content_type='application/json', status=404)

async def banner_get_api(request):
    """
    key: banners
    value:
        {
            "_banners": [{
                "img": "图片外链",
                "url": "图片指向的链接",
                "num": "图片排序",
                "update": "更新时间"
            }, {......}],
        }
    """
    pool = await aioredis.create_pool(REDISHOST, REDISPORT)
    async with pool as redis:
        banners = await redis.get('banners')
        banners_dict = ast.literal_eval(banners)
        banners_list = banners.get('_banners')
        return web.json_response(sorted(banners_list, key=lambda x: int(x['num'])))

@require_admin_login
async def banner_add_api(request):
    json_data = await request.json()
    pool = await aioredis.create_pool(REDISHOST, REDISPORT)
    async with pool as redis:
        update = time.time()
        json_data.update({'update': update})
        await redis.set('banners', json_data)
        return web.Response(body=b'{}', content_type='application/json', status=201)

@require_admin_login
async def banner_del_api(request):
    img = request.rel_url.query['name']  # 待删除banner的图片外链
    pool = await aioredis.create_pool(REDISHOST, REDISPORT)
    async with pool as redis:
        banners = await redis.get('banners')
        banners_dict = ast.literal_eval(banners)
        banners_list = banners_dict.get('_banners')
        for banner in banners_list:
            if banner['img'] == img:
                banners_list.remove(banner)
                await redis.set('banners', banners_list)
                return web.json_response({})
            return web.Response(b'{}', content_type='application/json', status=404)

@require_admin_login
async def banner_update_api(request):
    json_data = await request.json()
    img = json_data.get('img')
    num = json_data.get('num')
    pool = await aioredis.create_pool(REDISHOST, REDISPORT)
    async with pool as redis:
        banners = await redis.get('banners')
        banners_dict = ast.literal_eval(banners)
        banners_list = banners_dict.get('_banners')
        for banner in banners_list:
            if banner['img'] == img:
                banner['num'] = num  # 更新排序num
                await redis.set('banners', banners_list)
                return web.json_response({})
            return web.Response(b'{}', content_type='application/json', status=404)

async def calendar_get_api(request):
    """
    key: calendar
    value: {
        'img': '校历图片七牛外链',
        'size': '校历图片大小',
        'update': '更新时间戳'
    }
    """
    pool = await aioredis.create_pool(REDISHOST, REDISPORT)
    async with pool as redis:
        calendar = await redis.get('calendar')
        return web.json_response(ast.literal_eval(calendar))

@require_admin_login
async def calendar_update_api(request):
    json_data = await request.json()
    pool = await aioredis.create_pool(REDISHOST, REDISPORT)
    async with pool as redis:
        await redis.set('calendar', json_data.update({'update': time.time()}))
        return web.Response(b'{}', content_type='application/json', status=201)

async def start_get_api(request):
    """
    key: start
    value: {
        'img': '闪屏图片七牛外链',
        'url': '图片指向的链接',
        'update': '闪屏更新时间戳'
    }
    """
    pool = await aioredis.create_pool(REDISHOST, REDISPORT)
    async with pool as redis:
        start = await redis.get('start')
        return web.json_response(ast.literal_eval(start))

@require_admin_login
async def start_update_api(request):
    json_data = await request.json()
    pool = await aioredis.create_pool(REDISHOST, REDISPORT)
    async with pool as redis:
        update = time.time()
        await redis.set('start', json_data.append({'update': update}))
        return web.Response(b'{}', content_type='application/json', status=201)

api.router.add_route('GET', '/apartment/', apartment_info_api, name='apartment_info_api')
api.router.add_route('GET', '/product/', product_get_api, name='product_get_api')
api.router.add_route('PUT', '/product/', product_add_api, name='product_add_api')
api.router.add_route('DELETE', '/product/', product_del_api, name='product_del_api')
api.router.add_route('GET', '/banner/', banner_get_api, name='banner_get_api')
api.router.add_route('POST', '/banner/', banner_add_api, name='banner_add_api')
api.router.add_route('DELETE', '/banner/', banner_del_api, name='banner_del_api')
api.router.add_route('PUT', '/banner/', banner_update_api, name='banner_update_api')
api.router.add_route('GET', '/calendar/', calendar_get_api, name='calendar_get_api')
api.router.add_route('POST', '/calendar/', calendar_update_api, name='calendar_update_api')
api.router.add_route('GET', '/start/', start_get_api, name='start_get_api')
api.router.add_route('POST', '/start/', start_get_api, name='start_get_api')
