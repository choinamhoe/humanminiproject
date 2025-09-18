from sqlalchemy import create_engine
from config.config import config

db_info = f"mysql+pymysql://{config['DB_ID']}:{config['DB_PW']}@{config['HOST']}:{config['PORT']}/{config['DB_NAME']}"
engine = create_engine(db_info,connect_args={})
