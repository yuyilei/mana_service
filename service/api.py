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
        banners = await redis.hgetall('banners')
        banners_dict = ast.literal_eval(banners)
        banners_list = banners.get('_banners')
        return web.json_response(banners_list)

async def banner_add_api(request):
    json_data = await request.json()
    pool = await aioredis.create_pool(REDISHOST, REDISPORT)

api.router.add_route('GET', '/apartment/', apartment_info_api, name='apartment_info_api')
api.router.add_route('GET', '/product/', product_get_api, name='product_get_api')
api.router.add_route('PUT', '/product/', product_add_api, name='product_add_api')
api.router.add_route('DELETE', '/product/', product_del_api, name='product_del_api')
api.router.add_route('GET', '/banner/', banner_get_api, name='banner_get_api')
