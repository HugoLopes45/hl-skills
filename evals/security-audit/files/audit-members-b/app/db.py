import os

import psycopg
from flask import g
from psycopg.rows import namedtuple_row


def get_db() -> psycopg.Connection:
    if "db" not in g:
        g.db = psycopg.connect(os.environ["DATABASE_URL"], row_factory=namedtuple_row)
    return g.db
