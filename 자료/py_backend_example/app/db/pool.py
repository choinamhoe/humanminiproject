from sqlalchemy import create_engine
from config.config import config
user_id=config["DB"]["USER_ID"]
password=config["DB"]["PASSWORD"]
host=config["DB"]["HOST"]
db_info = f"mysql+pymysql://{user_id}:{password}@{host}"
engine = create_engine(
    db_info,connect_args={}) 
