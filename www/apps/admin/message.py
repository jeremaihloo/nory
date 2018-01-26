import aiohttp
from aiohttp import web
import logging
from infrastructures.apps import features
from infrastructures.apps.decorators import feature

MESSAGE_TYPE_SNACK_BAR = 'MESSAGE_TYPE_SNACK_BAR'


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    request.app['websockets'].append(ws)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                message_entry = msg.data.split('|')
                for _ws in request.app['websockets']:
                    _ws.send_str(msg.data)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            logging.warning('message connection closed with exception %s' % ws.exception())

    request.app['websockets'].remove(ws)
    logging.info('admin message server connection closed')

    return ws


@feature(features.__FEATURE_ON_APP_LOADING__, 'start_admin_message_server', 'start_admin_message_server')
async def start_admin_message_server(app):
    app['websockets'] = []
    app.router.add_get('/manage/admin/message', websocket_handler)
