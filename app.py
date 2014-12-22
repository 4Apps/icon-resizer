#!/usr/bin/env python3

import argparse
import logging

from tornado.web import Application as TornadoApplication, RedirectHandler, url, StaticFileHandler
from tornado.ioloop import IOLoop

from settings import settings
from application.default import DefaultHandler
from application.uploads import UploadHandler


class Application(TornadoApplication):
    """ Tornado application expansion to initialize stuff like database and sessions """

    def __init__(self, handlers, **settings):
        TornadoApplication.__init__(self, handlers, **settings)


if __name__ == "__main__":
    """ Web server initialization """

    # Setup default logging level
    logging.getLogger().setLevel(logging.WARNING if settings['debug'] else logging.ERROR)

    # Parse commandline arguments
    parser = argparse.ArgumentParser(description='Web Application Starter')
    parser.add_argument('--port', type=int, default=settings['port'], help='Port')
    args = parser.parse_args()

    # Put current port in settings
    settings['port'] = args.port

    # Initialize our application
    application = Application([
        url(r"/upload", UploadHandler, name='Upload'),
        url(r"/", DefaultHandler, name='HomePage'),
        (r"/static/(.*)", StaticFileHandler, {"path": settings['static_path']}),
    ], **settings)

    # Start application loop
    application.listen(args.port, '0.0.0.0' if settings['debug'] else '127.0.0.1')
    IOLoop.instance().start()
