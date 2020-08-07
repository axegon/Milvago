"""We reffer to advanced routes as being able to
use parameters as a part of the uri. For instance
/users/Milvago and translating "Milvago" to a named
Parameter. There are plenty of options available inside
falcon, which you can directly access the same way.
Check https://falcon.readthedocs.io/en/stable/api/routing.html#default-router
for more details.


Here is what you should expect from this script:

$ curl 'http://localhost:8000/'

    The output you should get is:
    Hello Milvago!

$ curl 'http://localhost:8000/users/Linus'

    The output you would get is:
    Looking at the profile of Linus

$ curl 'http://localhost:8000/purchases/Linus'

    The output you would get is:
    User Linus has purchased 46.87389222100248 Euros.

"""
import hashlib
from milvago import expose_web, Milvago, HttpMlv


@expose_web('/')
def index(web):
    return 'Hello Milvago!'

@expose_web("/user/{username}", 'get')
def show_user_profile(web):
    user = web.uri_data["username"]
    return f"Looking at the profile of {user}\n"


class AdvancedRoutingUserPurchases(HttpMlv):

    def __init__(self):
        HttpMlv.__init__(self, '/user/purchases/{username}')

    def get(self):
        username = self.uri_data.get("username")
        return f"User {username} has purchased " \
               f"{16 ** 32 / int(hashlib.md5(username.encode()).hexdigest(), 16) * 33} " \
               f"Euros.\n"


milvago = Milvago(
    [
        index(),
        show_user_profile(),
        AdvancedRoutingUserPurchases()
    ],
    debug=True)
server = milvago()
