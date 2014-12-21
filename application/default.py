
from application.base import BaseHandler


class DefaultHandler(BaseHandler):

    def get(self):
        self.render('index.html');

