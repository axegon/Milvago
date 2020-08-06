'''

 Milvago
    - A genus of bird of prey in the family Falconidae.
                 .------._
           .-````-.<')    `-.___
          (.----. _             '---.__.-
              __---'
            .---'``
             `""'-,
                   ````

This is a simplified interface for the falcon web framework with a built-in
support for jinja2 templates: The same performance without the boilerplate
code.



The most simple of examples, let's call it uber_simple.py
---------------------------------------------------------
from milvago import expose_web, Milvago


@expose_web('/')
def index(web):
    return 'Hello Milvago!'


milvago = Milvago([index()], debug=True)
server = milvago()

---------------------------------------------------------
You can start the server by running $ python uber_simple.py
The example above will run the application in development mode
through wsgiref. If you want to run it in production, you should

1. Change
    milvago = Milvago([index()], debug=True)
    to
    milvago = Milvago([index()], debug=False)
2. Run it with gunicorn:
    gunicorn uber_simple:server
'''

from milvago.server.handlers import HttpMlv, HttpStaticDir, API, expose_web, expose_static
from milvago.server.collector import Milvago
from milvago.__version__ import __version__
