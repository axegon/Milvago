import cherrypy
from common_data import CONTENTS


class benchmark:
    @cherrypy.expose
    def index(self):
        cherrypy.response.headers['Content-type'] = 'application/json'
        return CONTENTS.encode()


if __name__ == '__main__':
    cherrypy.quickstart(benchmark())