from flask import Flask, render_template, jsonify, request, abort, Request, redirect, url_for
from db.db_connector import DatabaseConnector
from db.queries import fetch_jobs_from_db, fetch_job_by_id, save_candidates
from sqlalchemy import text
import os

app = Flask(__name__)
# secret key required to store session data
app.secret_key = os.urandom(24)
# global db connector
db_connector = DatabaseConnector()

@app.route("/")
def hello_world():
    db_session = db_connector.init_session()
    JOBS = fetch_jobs_from_db(db_session)
    db_session = db_connector.close_session()
    return render_template('home.html', 
                           jobs=JOBS)

@app.route("/job/<id>")
def render_concrete_job(id):
    # python sometimes buffers output (e.g when app is running in the Docker),
    # the flush forces to output a print
    # print("APP MAIN", flush=True)
    db_session = db_connector.init_session()
    job = fetch_job_by_id(db_session, int(id))
    db_session = db_connector.close_session()
    if not job:
        # exception handler in flask
        abort(404)
    return render_template('job_page.html',
                           job=job)

@app.route("/submit_form", methods=['POST'])
def submit_form():
    db_session = db_connector.init_session()
    response = save_candidates(db_session, request)         # save_candidates() returns Response object (from redirect() function)
    db_session = db_connector.close_session()
    return response

if __name__ == "__main__":
    app.run('0.0.0.0', port=7777, debug=True)