#!/usr/bin/env python3

import argparse

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

    # Parse commandline arguments
    parser = argparse.ArgumentParser(description='ios-icons')
    parser.add_argument('--port', type=int, default=4000, help='Port')
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
    application.listen(args.port)
    IOLoop.instance().start()
