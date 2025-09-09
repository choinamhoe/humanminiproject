from sqlalchemy import create_engine

def get_connection():
    user_id = "root"
    password = "15932!miniprojectdb"
    host = "192.168.0.41"
    port = 30000
    database_name = "miniproject"
    db_info = f"mysql+pymysql://{user_id}:{password}@{host}:{port}/{database_name}"
    engine = create_engine(
    db_info, connect_args={}) 
    return engine
