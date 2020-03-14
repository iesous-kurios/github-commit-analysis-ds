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
    curs = conn.cursor()
    for i in range(len(data2)):
        insert = ("INSERT INTO PullRequests VALUES (" +
                    "'" + str(variables['name']) +"'" +  ", " +
                    "'" + str(variables['owner']) +"'" +  ", " + 
                    "'" + str(data[i]['id']) +"'" +  ", " +
                    "'" + str(data[i]['state']) +"'" +  ", " + 
                    "'" + str(data[i]['createdAt']) + "'" + ", " +
                    "'" + str(data[i]['closedAt']) + "'" +  ", " +
                    "'" + str(data[i]['title'].replace("'","")) +"'" +  ", " + 
                    "'" + str(data[i]['bodyText'].replace("'","")) +"'" +  ", " +
                    "'" + str(data[i]['author']['login']) +"'" +  ", " + 
                    "'" + str(data[i]['participants']['totalCount']) +"'" +  ", " + 
                    "'" + str(data[i]['comments']['totalCount']) +"'" +  ", " + 
                    "'" + str(data[i]['reactions']['totalCount'])+"'" + ", " +
                    "'" + str(data[i]['commits']['totalCount']) +"'" +  ", " + 
                    "'" + str(data[i]['changedFiles']) +"'" +  ", " +
                    "'" + str(data[i]['additions']) +"'" +  ", " + 
                    "'" + str(data[i]['deletions']) + "'" +  ") ON CONFLICT (ID) DO NOTHING")
        curs.execute(insert)
    
    conn.commit()