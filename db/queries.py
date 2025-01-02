from flask import flash, redirect, url_for, request, jsonify, Request, abort
from sqlalchemy import text
from sqlalchemy.orm import Session
from werkzeug.datastructures import ImmutableMultiDict
from db.models import Base, Candidates


def fetch_jobs_from_db(session: Session) -> list[dict]:
   with session as conn:
      # PostreSQL treats unquoted table names as lowercase by default so, in this case Jobs is transformed to jobs!
      result = conn.execute(text("select * from Jobs"))
      result_dicts = []
      # result.all() if SQLAlachemy.Row instance, so we need to convert it into dict()
      for row in result.all():
         result_dicts.append(row._asdict())
   return result_dicts

def fetch_job_by_id(session: Session, job_id: int) -> dict | None:
    with session as conn:
        result = conn.execute(text("select * from Jobs where id=:job_id"), {"job_id":job_id})
        row = result.first()
        if row:
           # cast row to dict(); note: we always try to cast on the types known to us
           return row._asdict()
    return None

def save_candidates(session: Session, request: Request) -> None:
    # getting ImmutableDict key-values from request body (request data)
    # note: GET request 'data' is sent in the URL query params and get by request.args.get()
    form_data = request.form
    
    print("FORM: ", form_data, flush=True)
    name = form_data['name']
    surname = form_data['surname']
    email = form_data['email']
    # these 3 are required
    if not all([name, surname, email]):
        abort(404, "Name, surnmame and e-mail are required!")
    try:
        with session as conn:
            new_candidate = Candidates(
                name=form_data['name'],
                surname=form_data['surname'],
                adress1=form_data['address1'],
                adress2=form_data['address2'],
                city=form_data['city'],
                email=form_data['email'],
                state=form_data['state'],
                zip_code=form_data['zip_code'],
                # job_id from the 'jobs' table as Foreign Key
                job_id=form_data['job_id'])
            conn.add(new_candidate)
            conn.commit()
            # flashes message to the user; (job_page.html renders it)
            flash("Adding candidate was successful!", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        # 'render_concrete_job' is the name of the function, and id is the param
    return redirect(url_for('render_concrete_job', id=request.form.get('job_id')))
    

