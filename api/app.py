from flask import Flask, Response
from flask import jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import requests
from dotenv import load_dotenv
from api.utils import update_pull_requests, sentiment

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

    @app.route('/getall')
    def get_all():
        query = ("SELECT * FROM PullRequests")
        conn = psycopg2.connect(database=db, user=usern,
                                password=passw, host=host,
                                port=port,
                                cursor_factory=RealDictCursor)
        curs = conn.cursor()
        curs.execute(query)
        return jsonify(curs.fetchall())

    @app.route('/getPRs/<owner>/<repo>')
    def get_PRs(owner, repo):
        query = ("SELECT * FROM PullRequests "
                 "WHERE ownername = '" + owner + "' "
                 "AND reponame = '" + repo + "';")
        conn = psycopg2.connect(database=db, user=usern,
                                password=passw, host=host,
                                port=port,
                                cursor_factory=RealDictCursor)
        curs = conn.cursor()
        curs.execute(query)
        return jsonify(curs.fetchall())

    @app.route('/getclosed/<owner>/<repo>')
    def get_closed(owner, repo):
        query = ("SELECT ownername, reponame, state, CreatedAt, ClosedAt, "
                 "(EXTRACT(epoch FROM ("
                 "TO_TIMESTAMP(ClosedAt, 'YYYY-MM-DD HH24:MI:SS'))) - "
                 "EXTRACT(epoch FROM ("
                 "TO_TIMESTAMP(CreatedAt, 'YYYY-MM-DD HH24:MI:SS'))))"
                 "AS diff FROM PullRequests "
                 "WHERE (state='CLOSED' "
                 "OR state='MERGED') "
                 "AND ownername = '" + owner + "' "
                 "AND reponame = '" + repo + "';")
        conn = psycopg2.connect(database=db, user=usern,
                                password=passw, host=host,
                                port=port,
                                cursor_factory=RealDictCursor)
        curs = conn.cursor()
        curs.execute(query)
        return jsonify(curs.fetchall())

    @app.route('/getmetadata')
    def get_metadata():
        query = """
              SELECT "table_name","column_name", "data_type", "table_schema"
              FROM INFORMATION_SCHEMA.COLUMNS
              WHERE "table_schema" = 'public'
              ORDER BY table_name"""
        conn = psycopg2.connect(database=db, user=usern,
                                password=passw, host=host,
                                port=port,
                                cursor_factory=RealDictCursor)
        curs = conn.cursor()
        curs.execute(query)
        return jsonify(curs.fetchall())

    @app.route('/summarize/<owner>/<repo>')
    def summarize(owner, repo):
        conn = psycopg2.connect(database=db, user=usern,
                                password=passw, host=host,
                                port=port,
                                cursor_factory=RealDictCursor)
        query = ("SELECT (SELECT AVG(EXTRACT(epoch FROM ("
                 "TO_TIMESTAMP(ClosedAt, 'YYYY-MM-DD HH24:MI:SS'))) - "
                 "EXTRACT(epoch FROM ("
                 "TO_TIMESTAMP(CreatedAt, 'YYYY-MM-DD HH24:MI:SS'))))/86400 "
                 "FROM PullRequests "
                 "WHERE state in ('MERGED', 'CLOSED') "
                 "AND ownername = '" + owner + "' "
                 "AND reponame = '" + repo + "') "
                 "AS mean_days_to_merge_or_close, "
                 "(SELECT AVG(EXTRACT(epoch FROM ("
                 "TO_TIMESTAMP(ClosedAt, 'YYYY-MM-DD HH24:MI:SS'))) - "
                 "EXTRACT(epoch FROM ("
                 "TO_TIMESTAMP(CreatedAt, 'YYYY-MM-DD HH24:MI:SS'))))/86400 "
                 "FROM PullRequests "
                 "WHERE state = 'MERGED' "
                 "AND ownername = '" + owner + "' "
                 "AND reponame = '" + repo + "') "
                 "AS mean_days_to_merge, "
                 "(SELECT AVG(EXTRACT(epoch FROM ("
                 "TO_TIMESTAMP(ClosedAt, 'YYYY-MM-DD HH24:MI:SS'))) - "
                 "EXTRACT(epoch FROM ("
                 "TO_TIMESTAMP(CreatedAt, 'YYYY-MM-DD HH24:MI:SS'))))/86400 "
                 "FROM PullRequests "
                 "WHERE state = 'CLOSED' "
                 "AND ownername = '" + owner + "' "
                 "AND reponame = '" + repo + "') "
                 "AS mean_days_to_close, "
                 "(SELECT AVG(EXTRACT(epoch FROM now()) - "
                 "EXTRACT(epoch FROM ("
                 "TO_TIMESTAMP(CreatedAt, 'YYYY-MM-DD HH24:MI:SS'))))/86400 "
                 "FROM PullRequests WHERE state='OPEN' "
                 "AND ownername = '" + owner + "' "
                 "AND reponame = '" + repo + "') "
                 "AS mean_days_age_open_prs, "
                 "(CAST(SUM(CASE WHEN state = 'MERGED' THEN 1 ELSE 0 END) "
                 "AS float)) / "
                 "NULLIF (SUM(CASE WHEN state IN ('MERGED', 'CLOSED') "
                 "THEN 1 ELSE 0 END), 0) * 100 "
                 "AS percent_merged "
                 "FROM PullRequests "
                 "WHERE ownername = '" + owner + "' "
                 "AND reponame = '" + repo + "';")
        curs = conn.cursor()
        curs.execute(query)
        avg = {'average_sentiment':sentiment(conn, repo)}
        return jsonify([curs.fetchall(), avg])

    @app.route('/updatePRs/<owner>/<repo>', methods=['GET'])
    def updating(owner, repo):
        conn = psycopg2.connect(database=db, user=usern,
                                password=passw, host=host,
                                port=port,
                                cursor_factory=RealDictCursor)
        return Response(update_pull_requests(conn, owner, repo))

    return app
