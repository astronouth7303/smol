#!/usr/bin/env python
import asyncio
import logging
import pathlib
from aiohttp import web
from .webview import WebviewThread
from .server import setup_routes
import aiohttp_jinja2
import jinja2

PROJ_ROOT = pathlib.Path(__file__).parent


async def init(loop):
    # setup application and extensions
    app = web.Application(loop=loop, debug=True)

    aiohttp_jinja2.setup(
        app, loader=jinja2.PackageLoader('smol', 'templates'))
    # setup views and routes
    setup_routes(app, PROJ_ROOT)
    #setup_middlewares(app)

    return app


def main():
    # init logging
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init(loop))
    wv = WebviewThread('Test', 'http://localhost:9753/')
    @wv.onclose
    def exit():
        loop.stop()
    loop.call_soon(wv.start)
    # We can make this timeout super low because we exit when our only client exits
    web.run_app(app, host='localhost', port=9753, shutdown_timeout=1)
