import pymysql
import functools
from flask import jsonify, request
from flask_api import status
import flask
import boto3
import json


#local imports
from app import app


lambda_client = boto3.client('lambda')

class MySqlConn:
    def __init__(self):
        connection_options = {
            'host': 'localhost',
            'user': 'chends',
            'password': '8888',
            'database': 'jobsdb'}
        self.connection = pymysql.connect(**connection_options)

    def run(self, query, args=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, args)
            return cursor.fetchall()

def run_job(uid, code, paramenters):
    sqlconn = MySqlConn()
    sqlconn.run('INSERT INTO job (jobstatus, response, uid) VALUES ("RUNNING", NULL, %d);' %(uid))
    sqlconn.connection.commit()
    lastid = sqlconn.run('SELECT LAST_INSERT_ID();')[0][0]
    invoke_response = lambda_client.invoke(FunctionName='jobs', Payload=bytes(json.dumps({'code':code, 'input': paramenters}), 'utf-8'))
    payload = invoke_response['Payload'].read()
    payload = payload.decode('utf-8')
    if payload[1] == '0':
        payload = payload.split('"')[1]
        payload = payload[:-2]
        sqlconn.run('UPDATE job SET job.jobstatus="%s", job.response="%s" WHERE job.id=%d' %('DONE',str(payload) , lastid))
        sqlconn.connection.commit()
        return jsonify([{'job_id': lastid}])
    else:
        print('Error while executing code')
        sqlconn.run('UPDATE job SET job.jobstatus="%s" WHERE job.id=%d' %('ERROR', lastid))
        sqlconn.connection.commit()
        return jsonify([{'job_id': lastid}])

def get_jobs():
    sqlconn = MySqlConn()
    jobinfo = sqlconn.run('SELECT * FROM job')
    jobs = []
    for i in jobinfo:
        jobs.append({'job_id': i[0], 'uid': i[3], 'status': i[1], 'result': i[2]})
    return jsonify(jobs)

@app.route('/test', methods=['GET'])
def test():
    res = run_job()
    return jsonify(res)

@app.route('/', methods=['GET'])
def jobs2():
    return get_jobs()

@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    if (request.method == 'GET'):
        return get_jobs()
    elif (request.method == 'POST'):
        req = request.get_json(silent=True)
        return run_job(req['uid'], req['code'], req['input'])

@app.route('/jobs/<job_id>', methods=['GET'])
def list_job(job_id):
    try:
        int(job_id)
    except:
        return ('Job_id is not int')
    sqlconn = MySqlConn()
    jobinfo = sqlconn.run('SELECT * FROM job WHERE id=%s' %(job_id))
    jobs = []
    for i in jobinfo:
        jobs.append({'job_id': i[0], 'uid': i[3], 'status': i[1], 'result': i[2]})
    return jsonify(jobs)

@app.route('/users/<uid>', methods=['GET'])
def list_userjobs(uid):
    sqlconn = MySqlConn()
    userjobs = sqlconn.run('SELECT * FROM job WHERE uid=%s' %(uid))
    jobs = []
    for i in userjobs:
        jobs.append({'job_id': i[0], 'uid': i[3], 'status': i[1], 'result': i[2]})
    return jsonify(jobs)

'''
AWS LAMBDA CODE
# https://realpython.com/code-evaluation-with-aws-lambda-and-api-gateway/
import sys
from io import StringIO
import json

def lambda_handler(event, context):
    # get code from payload
    code = event['code']
    # capture stdout
    buffer = StringIO()
    sys.stdout = buffer
    # execute code
    try:
        exec(code, event['input'])
        return (0, buffer.getvalue())
    except Exception as e:
        # return (0, event['input'])
        return (1, e)
'''