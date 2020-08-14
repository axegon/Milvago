import milvago
from common_data import CONTENTS


@milvago.expose_web('/')
def benchmark(web):
    web.set_content_type("json")
    return CONTENTS

server = milvago.Milvago([benchmark()], debug=False)
srv = server()