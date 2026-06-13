import os
from pathlib import Path

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-me'
    
    # Use DATABASE_URL from environment if set, otherwise use instance path
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # Use absolute path within app.instance_path
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(Path(basedir) / 'instance' / 'squalo.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
