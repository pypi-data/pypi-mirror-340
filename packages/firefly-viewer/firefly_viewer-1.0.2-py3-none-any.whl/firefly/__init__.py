"""
Firefly Database Viewer
A Flask-based web interface for viewing and interacting with Firefly databases.
"""

import os
from flask import Flask
from .config import *
from .database import DatabaseClient
from .routes import routes
from .services import KeyService
from .logger import logger

def create_app():
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
    app = Flask(__name__, template_folder=template_dir)
    app.debug = DEBUG
    app.register_blueprint(routes)
    return app

app = create_app()

__version__ = "1.0.0"