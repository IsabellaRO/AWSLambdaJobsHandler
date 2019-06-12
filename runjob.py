import sys
sys.path.append('../')
import app

import pymysql
import json


client = app.app.test_client()
def test_runjob():
    '''
    Function parameters (ex: {'a': 1, 'b': 2})
    '''
    parameters = {'arg1': 1, 'arg2': 2}
    file = './' + sys.argv[2]
    with open(file, 'r', encoding='utf-8') as file:
        lines = file.read()
    data = client.post('/jobs', json={'uid': int(sys.argv[1]), 'code': lines, 'input': parameters})
    data = json.loads(data.data)
    print(data)

test_runjob()