from datetime import datetime
from decouple import config
from flask import Flask
from flask import request
import psycopg2
import pandas as pd
import os
import requests
from dotenv import load_dotenv
from .utils import pull_repo, summarize_PRs, run_query, update_pull_requests
from .queries import repo_query, initial_PR_query, cont_PR_query

load_dotenv(override=True)
host = os.getenv('RDS_HOSTNAME')
port = os.getenv('RDS_PORT')
db = os.getenv('RDS_DB_NAME')
usern = os.getenv('RDS_USERNAME')
passw = os.getenv('RDS_PASSWORD')

SECRET = os.getenv('SECRET')
URL = 'https://api.github.com/graphql'
DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

def runQuery(query, variables):
    r = requests.post(URL,
                      headers={'Authorization': 'token ' + SECRET, },
                      json={'query': query,
                            'variables': variables
                            })
    return r

def createApp():

    app = Flask(__name__)
    
    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    @app.route('/updatePRs/<owner>/<name>', methods=['GET'])
    def updating(owner=None, name=None, message='Enter an owner and repo name!'):
        owner = owner or request.args.get('owner')
        name = name or request.args.get('name')
        conn = psycopg2.connect(database=db, user=usern,
                                password=passw, host=host,
                                port=port)
        time_to_close = """SELECT AVG(TO_TIMESTAMP(ClosedAt, 'YYYY-MM-DD HH24:MI:SS')-TO_TIMESTAMP(CreatedAt, 'YYYY-MM-DD HH24:MI:SS'))
                        as diff FROM PullRequests"""
        update_pull_requests(conn,owner,name)
        curs = conn.cursor()
        curs.execute(time_to_close)
        pr_close_time = curs.fetchall()
        return f'The average time to close for a pull requests in {name} is {pr_close_time}'


    return app