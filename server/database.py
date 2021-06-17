import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_user = os.getenv("db_user", "root")
db_password = os.getenv("db_password", "example_password")
db_host = os.getenv("db_host", "0.0.0.0")
db_port = os.getenv("db_port", "3306")
#db_database = os.getenv("db_database", "")

db_connection_retries = os.getenv("db_connection_retries", "3")
db_connection_retry_timeout = os.getenv("db_connection_retry_timeout", "5")

# engine = create_engine("mysql+pymysql://{}:{}@{}:{}".format(
#     db_user, db_password, db_host, db_port
# ))

engine = create_engine(f'sqlite:///messenger.db')

# try to get connection to database
# if cannot program will die here
engine.execute(r"CREATE DATABASE IF NOT ESIST messenger")
engine.execute(r"USE messenger")

Base = declarative_base()

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)