from sqlalchemy import create_engine
from config.config import config
user_id=config["DB"]["USER_ID"]
password=config["DB"]["PASSWORD"]
host=config["DB"]["HOST"]
PORT=config["DB"]["PORT"]
DATABASE_NAME=config["DB"]["DATABASE_NAME"]
db_info = f"mysql+pymysql://{user_id}:{password}@{host}:{PORT}/{DATABASE_NAME}"
engine = create_engine(
    db_info,connect_args={}) 
