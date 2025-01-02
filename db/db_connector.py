from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from db.models import Base, Candidates, Jobs

load_dotenv()

class DatabaseConnector:
   db_user = os.getenv("PSQL_USER")
   db_password = os.getenv("PSQL_PASSWORD")
   db_host = os.getenv("PSQL_HOST")
   db_port = os.getenv("PSQL_PORT")
   db_name = os.getenv("PSQL_DEFAULT_DB")

   def __init__(self) -> None:
      self.db_url = f"postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
      self.engine = create_engine(url=self.db_url)
      self.Session = sessionmaker(self.engine)
      self.session = None
      # this line creates all objects related to the engine (Products, Products2, etc)
      Base.metadata.create_all(self.engine)
   def close_session(self):
      if self.session:
         # build-in sqlalchemy's orm method
         self.session.close()
         self.session = None
    
   def init_session(self):
      if not self.session:
         self.session = self.Session()
      return self.session
       