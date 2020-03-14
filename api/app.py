from datetime import datetime
from decouple import config
from flask import Flask
from flask import request
from .utils import pull_repo, summarize_PRs, run_query
import pandas as pd
import os
import requests
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
    def updating(owner='scikit-learn', name='scitkit-learn', message='Enter an owner and repo name!'):
        owner = owner or request.values['owner']
        name = name or request.values['name']
        conn = psycopg2.connect(database=db, user=usern,
                                password=passw, host=host,
                                port=port)
        update_pull_requests(conn,owner,name)
        pr_close_time = conn.cursor.execute(time_to_close)
        return pr_close_time


    return app