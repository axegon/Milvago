from milvago import expose_web, Milvago


@expose_web('/')
def index(web):
    return 'Hello Milvago!'


milvago = Milvago([index()], debug=True)
server = milvago()
