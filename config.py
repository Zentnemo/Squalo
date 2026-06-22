import os
from pathlib import Path

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-me'

    # ── Database: PostgreSQL in production, SQLite locally ─────────
    # Render sets DATABASE_URL automatically when you add a PostgreSQL
    # database add-on.  Older Render URLs start with "postgres://" which
    # SQLAlchemy 1.4+ no longer accepts – rewrite to "postgresql://".
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # Local dev fallback – SQLite
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(Path(basedir) / 'instance' / 'squalo.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── Public base URL for absolute links (emails, SEO, calendar) ──
    # Set on Render to e.g. https://squalo-schwimmcoaching.com
    # Locally: leave unset, falls back to request.host_url
    PUBLIC_BASE_URL = os.environ.get('PUBLIC_BASE_URL', '').rstrip('/')
