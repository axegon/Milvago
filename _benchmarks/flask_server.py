from flask import Flask, Response
from common_data import CONTENTS
app = Flask(__name__)

@app.route('/')
def hello_world():
    return Response(CONTENTS, mimetype='application/json')