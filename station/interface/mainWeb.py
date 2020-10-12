#!/usr/bin/python3
from flaskApp import app, db_conn

if __name__ == '__main__':
    db_conn.create_all()
    app.debug = False
    app.run()
