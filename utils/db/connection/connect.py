from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()


def db_connect():
    connection_string = os.environ.get("STRING_SQL")
    engine = create_engine(connection_string)
    return engine
