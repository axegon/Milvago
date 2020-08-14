import hug
from common_data import CONTENTS


@hug.get('/')
@hug.format.content_type('application/json')
def happy_birthday():
    return CONTENTS