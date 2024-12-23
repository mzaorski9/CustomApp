from flask import Flask, render_template, jsonify
from db_connector import engine, fetch_jobs_from_db
from sqlalchemy import text


app = Flask(__name__)

@app.route("/")
def hello_world():
    JOBS = fetch_jobs_from_db()
    return render_template('home.html', 
                           jobs=JOBS,
                           company_name="XYZ")

@app.route("/jobs")
def render_jobs():
    jobs = fetch_jobs_from_db()
    return jsonify(jobs)


if __name__ == "__main__":
    app.run('0.0.0.0', port=7777, debug=True)
