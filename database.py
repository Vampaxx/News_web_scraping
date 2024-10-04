import os 
from dotenv import load_dotenv



from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


load_dotenv()
db_host     = os.getenv("db_host")
db_user     = os.getenv("db_user")
db_password = os.getenv("db_password")
db_name     = os.getenv("db_name")


DATABASE_URL    = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
engine          = create_engine(DATABASE_URL)
SessionLocal    = sessionmaker(autocommit   = False, 
                                autoflush   = False, 
                                bind        = engine)
Base            = declarative_base()

