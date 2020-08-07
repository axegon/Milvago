"""In this example we explore how to create
class based views which give just as many options
as the function-based ones but can be a lot more
expressive and flexible as far as the structure of
your code goes. In reality the function-based views
do the exact same thing and create classes under the
hood in the exact same manner.

The crucial thing here is the HttpMlv class.


Run the script and you can check it with the following
CURL requests:

$ curl http://localhost:8000

    The output you should get is:
    This is a GET request from a class-based view.

$ curl -X POST http://localhost:8000

    The output you should get is:
    This is a POST request from a class-based view.

$ curl http://localhost:8000/another_example

    The output you should get is:
    Here's another example.

$ curl -X POST http://localhost:8000/another_example

    We haven't defined a POST handler for this mount-point,
    so the response you should get is:
    A server error occurred.  Please contact the administrator.
"""
from milvago import Milvago, HttpMlv


class Index(HttpMlv):
    """This class will serve as an index mount-point of
    the application. What you need to do is extend
    HttpMlv and call it's constructor, with the
    mount-point as a second parameter.

    For every available method you want to expose, you
    need to create the respective class method:
    GET - def get(self):...
    POST - def post(self):...
    OPTIONS - def options(self):...
    etc...
    """
    def __init__(self):
        HttpMlv.__init__(self, "/")

    def get(self):
        """As explained in the class docstring,
        this is the handler for GET requests."""
        return "This is a GET request from " \
               "a class-based view.\n"

    def post(self):
        """And this for POST requests respectively."""
        return "This is a POST request from " \
               "a class-based view.\n"


class SomeOtherClass(HttpMlv):
    """For the sake of the example, here we are
    adding a second class."""
    def __init__(self):
        HttpMlv.__init__(self, "/another_example")

    def get(self):
        """This time only a GET request will be handled."""
        return "Here's another example.\n"


milvago = Milvago(
    [
        Index(),
        SomeOtherClass()
    ],
    debug=True)
classes = milvago()
