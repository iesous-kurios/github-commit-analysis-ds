import requests
import os
import psycopg2
import pandas as pd
import numpy as np
from flask import jsonify
from dotenv import load_dotenv

load_dotenv(override=True)
host = os.getenv('RDS_HOSTNAME')
port = os.getenv('RDS_PORT')
db = os.getenv('RDS_DB_NAME')
usern = os.getenv('RDS_USERNAME')
passw = os.getenv('RDS_PASSWORD')

conn = psycopg2.connect(database=db, user=usern,
                        password=passw, host=host,
                        port=port)
def updateDB(data, conn):
    '''Function takes in data returned from github apiv4
    as well as a postgresSQL connection object and pushed all
    pull requests contained in data to the repository, assuming their
    ids don't already exist'''
    data2 = data['data']['repository']['pullRequests']['nodes']
    curs = conn.cursor()
    for i in range(len(data2)):
        insert = ("INSERT INTO PullRequests VALUES (" +
                    "'" + str(variables['name']) +"'" +  ", " +
                    "'" + str(variables['owner']) +"'" +  ", " + 
                    "'" + str(data2[i]['id']) +"'" +  ", " +
                    "'" + str(data2[i]['state']) +"'" +  ", " + 
                    "'" + str(data2[i]['createdAt']) + "'" + ", " +
                    "'" + str(data2[i]['closedAt']) + "'" +  ", " +
                    "'" + str(data2[i]['title'].replace("'","")) +"'" +  ", " + 
                    "'" + str(data2[i]['bodyText'].replace("'","")) +"'" +  ", " +
                    "'" + str(data2[i]['author']['login']) +"'" +  ", " + 
                    "'" + str(data2[i]['participants']['totalCount']) +"'" +  ", " + 
                    "'" + str(data2[i]['comments']['totalCount']) +"'" +  ", " + 
                    "'" + str(data2[i]['reactions']['totalCount'])+"'" + ", " +
                    "'" + str(data2[i]['commits']['totalCount']) +"'" +  ", " + 
                    "'" + str(data2[i]['changedFiles']) +"'" +  ", " +
                    "'" + str(data2[i]['additions']) +"'" +  ", " + 
                    "'" + str(data2[i]['deletions']) + "'" +  ") ON CONFLICT (ID) DO NOTHING")
        curs.execute(insert)
    
    conn.commit()