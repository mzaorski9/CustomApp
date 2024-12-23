import sqlalchemy
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

db_user = os.getenv("PSQL_USER")
db_password = os.getenv("PSQL_PASSWORD")
db_host = os.getenv("PSQL_HOST")
db_port = os.getenv("PSQL_PORT")
db_name = os.getenv("PSQL_DEFAULT_DB")

db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(url=db_url)

def fetch_jobs_from_db():
   with engine.connect() as conn:
      result = conn.execute(text("select * from jobs"))
      result_dicts = []
      # result.all() if SQLAlachemy.Row instance, so we need to convert it into dict()
      for row in result.all():
         result_dicts.append(row._asdict())
   return result_dicts


