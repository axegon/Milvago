import time
import unittest
import threading
import requests
import milvago


@milvago.expose_web('/')
def index(web):
    return 'Hello!'


@milvago.expose_web('/get_only', 'get')
def get_only(web):
    return 'This is GET'


@milvago.expose_web('/post_only', 'post')
def post_only(web):
    return 'This is POST'


@milvago.expose_web('/post_and_get', 'post, get')
def post_and_get(web):
    return f'This is {web.request.method}'


class ContentTypes(milvago.HttpMlv):

    def __init__(self):
        milvago.HttpMlv.__init__(self, '/contenttypes')

    def get(self):
        self.set_content_type('json')
        return '{"msg": "Hey, I\'m mr. JSON, look at meee!"}'

print()
srv = milvago.Milvago(
    [
        index(),
        get_only(),
        post_only(),
        post_and_get(),
        ContentTypes()
    ],
    debug=True
)
T = threading.Thread(target=srv, daemon=True).start()
time.sleep(3.14)


class TestGeneral(unittest.TestCase):

    def test_get(self):
        self.assertEqual(requests.get('http://127.0.0.1:8000/').text, 'Hello!')
        self.assertEqual(requests.get('http://127.0.0.1:8000/get_only').text, 'This is GET')
        self.assertEqual(requests.get('http://127.0.0.1:8000/post_and_get').text, 'This is GET')

    def test_post(self):
        self.assertEqual(requests.post('http://127.0.0.1:8000/post_only').text, 'This is POST')
        self.assertEqual(requests.post('http://127.0.0.1:8000/post_and_get').text, 'This is POST')

    def test_content_type(self):
        self.assertEqual(
            requests.get('http://127.0.0.1:8000/contenttypes').headers.get('content-type'),
            'application/json'
        )