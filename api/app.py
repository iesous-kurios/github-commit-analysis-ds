from datetime import datetime

from flask import Flask
from flask import request

import pandas as pd
import os
import requests

SECRET = os.environ.get('SECRET')
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


    @app.route('/repository', methods=['GET', 'POST'])
    def repository():
        if request.method == 'GET':
            user = request.args.get('user')
            repo = request.args.get('repo')
        elif request.method == 'POST':
            req_json = request.get_json()
            user = req_json['user']
            repo = req_json['repo']

        query = '''
        query ($user: String!, $repo: String!){
            repository(owner: $user, name: $repo) {
                    name
                    owner {
                        login
                        }
                    description
                    primaryLanguage {
                        name
                        }
                    stars: stargazers {
                        totalCount
                        }
                    forks: forkCount
                    totalIssues: issues {
                        totalCount
                        }
                    openIssues: issues (states: [OPEN]) {
                        totalCount
                        }
                    closedIssues: issues (states: [CLOSED]) {
                        totalCount
                        }
                    vulnerabilityAlerts {
                        totalCount
                        }
                    totalPRs: pullRequests {
                        totalCount
                        }
                    openPRs: pullRequests (states: [OPEN]) {
                        totalCount
                        }
                    mergedPRs: pullRequests (states: [MERGED]) {
                        totalCount
                        }
                    closedPRs: pullRequests (states: [CLOSED]) {
                        totalCount
                        }
                    createdAt
                    updatedAt
                    diskUsage
                    pullRequests (last: 50) {
                    nodes {
                        author {
                            login
                            }
                        state
                        createdAt
                        closedAt
                        changedFiles
                        additions
                        deletions
                        }
                    }
                }
            }
            '''

        variables = {'user': user, 'repo': repo}

        data = runQuery(query, variables).json()['data']['repository']
        data['stars'] = data['stars']['totalCount']
        data['owner'] = data['owner']['login']
        data['primaryLanguage'] = data['primaryLanguage']['name']
        data['totalIssues'] = data['totalIssues']['totalCount']
        data['openIssues'] = data['openIssues']['totalCount']
        data['closedIssues'] = data['closedIssues']['totalCount']
        data['totalPRs'] = data['totalPRs']['totalCount']
        data['openPRs'] = data['openPRs']['totalCount']
        data['mergedPRs'] = data['mergedPRs']['totalCount']
        data['closedPRs'] = data['closedPRs']['totalCount']
        data['vulnerabilityAlerts'] = data['vulnerabilityAlerts']['totalCount']

        data['PRacceptanceRate'] = data['mergedPRs'] / (data['mergedPRs'] +
                                                        data['closedPRs'])
        data['createdAt'] = datetime.strptime(data['createdAt'],
                                            DATE_FORMAT)
        data['updatedAt'] = datetime.strptime(data['updatedAt'],
                                            DATE_FORMAT)
        data['ageInDays'] = (datetime.now().date() -
                            data['createdAt'].date()).days
        data['starsPerDay'] = data['stars'] / data['ageInDays']
        data['forksPerDay'] = data['forks'] / data['ageInDays']
        data['PRsPerDay'] = data['totalPRs'] / data['ageInDays']
        data['issuesPerDay'] = data['totalIssues'] / data['ageInDays']

        pull_requests = data['pullRequests']['nodes']
        del data['pullRequests']
        df = pd.DataFrame.from_records(pull_requests)
        df['author'] = [author.get('login') if author is not None else ''
                        for author in df['author']]
        df['createdAt'] = pd.to_datetime(df['createdAt'], format=DATE_FORMAT)
        df['closedAt'] = pd.to_datetime(df['closedAt'], format=DATE_FORMAT)

        data['uniquePRauthors'] = df['author'].nunique()

        return data
    return app