"""Here we'll explore how to access post and get
parameters from requests. In addition, we will
explore how to use function-based views for
different types of requests simultaneously.

Here is what you should expect from this script:

$ curl 'http://localhost:8000/?name=Milvago'

    The output you should get is:
    Hello Milvago!

$ curl 'http://localhost:8000/post_and_get'

    The output you should get is:
    So you are using a GET request.

$ curl -X POST 'http://localhost:8000/post_and_get'

    The output you should get is:
    POST this time?

$ curl -X PUT 'http://localhost:8000/post_and_get'

    The output you should get is:
    PUT? I didn't expect that.

$ curl -X DELETE 'http://localhost:8000/post_and_get'

    The output you should get is:
    A server error occurred.  Please contact the administrator.

$ curl 'http://localhost:8000/class_post_get?name=Milvago'

    The output you should get is:
    Hello, Milvago

$ curl -X POST 'http://localhost:8000/class_post_get' --data "message=People with courage and character always seem sinister to the rest."

    The output you should get is:
    Here's your message:
        People with courage and character always seem sinister to the rest.

"""

from milvago import expose_web, Milvago, HttpMlv


@expose_web('/')
def index(web):
    """The web.request.params is a dictionary,
    pointing to falcon.Request directly."""
    name = web.request.params["name"]
    return f"Hello {name}!\n"


@expose_web('/post_and_get', 'get, post, put')
def post_and_get(web):
    """The expose_web decorator accepts a second
    parameter, which is a comma-separated string
    of all the methods you want to expose. How
    they are handled however, needs to be implemented
    in your function."""
    method = web.request.method
    if method == "GET":
        return "So you are using a GET request.\n"
    elif method == "POST":
        return "POST this time?\n"
    else:
        return f"{method}? I didn't expect that.\n"


class ClassBasedPostGet(HttpMlv):
    """The above two functions in reality generate
    a class such as this one, with the exception that
    here all methods have individual implementation,
    whereas in the examples above, the get, post and
    whatever other request methods you might use
    are replicated."""
    def __init__(self):
        HttpMlv.__init__(self, '/class_post_get')

    def get(self):
        name = self.request.params["name"]
        return f"Hello, {name}\n"

    def post(self):
        message = self.request.params["message"]
        return f"Here's your message:\n\t{message}\n"


milvago = Milvago(
    [
        index(),
        post_and_get(),
        ClassBasedPostGet()
    ],
    debug=True)
server = milvago()
