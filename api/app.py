from datetime import datetime
from decouple import config
from flask import Flask
from flask import request
from .utils import pull_repo, summarize_PRs, run_query
import pandas as pd
import os
import requests
from .queries import repo_query, initial_PR_query, cont_PR_query

SECRET = config('SECRET')
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

    @app.route('/test')
    def test_data():
        variables = {'owner': 'scikit-learn', 'name': 'scikit-learn'}
        response = run_query(initial_PR_query, variables)
        data = response.json()['data']['repository']
        data['name'] = variables['name']
        data['owner'] = variables['owner']
        return data


    @app.route('/repository', methods=['GET', 'POST'])
    def get_repo_summ():
        data = pull_repo('scikit-learn','scikit-learn')
        summ_data = summarize_PRs(data)
        return summ_data

    return app