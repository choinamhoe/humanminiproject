from db.pool import engine
from sqlalchemy import create_engine, text

def get_hello_message():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT message FROM hello_table LIMIT 1"))
        row = result.fetchone()
        if row:
            return {"message": row[0]}
        return {"message": "데이터 없음"}