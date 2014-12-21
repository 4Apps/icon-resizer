import json
from tornado.web import RequestHandler

class BaseHandler(RequestHandler):
    def error(self, message):
        if isinstance(message, dict):
            message = json.dumps(message)
        self.write(message)


    @property
    def context(self):
        if not hasattr(self, '_context'):
            self._context = {
                'settings': self.settings,
            }
        return self._context



    def render(self, template, **kwargs):
        self.context.update(kwargs)
        return super(BaseHandler, self).render(template, **self.context)



    def get(self):
        self.error({'error': {'code': -1, 'msg': 'Method not implemented'}})


    def post(self):
        self.error({'error': {'code': -2, 'msg': 'Method not implemented'}})
