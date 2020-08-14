import tornado.ioloop
import tornado.web
from common_data import CONTENTS

class Index(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-type', 'application/json')
        self.write(CONTENTS)

def make_app():
    return tornado.web.Application([
        (r"/", Index),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
