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