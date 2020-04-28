""" Main application for Hacker News Trolls """
import numpy as np
import pandas as pd
from decouple import config
from flask import Flask, json, jsonify, request, send_file, render_template
import psycopg2

def create_app():
    """Create and config routes"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['ENV'] = 'debug'  # TODO change before deployment
