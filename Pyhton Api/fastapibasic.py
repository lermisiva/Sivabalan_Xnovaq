from fastapi import FastAPI , HTTPException 
from pydantic import BaseModel
import snowflake.connector

app = FastAPI(title= 'MysampleAPI')

conn_params = {
    'user': 'Sivabalan0007',
    'password': 'Sivabalan@3252',
    'account': 'ko81895.me-central2.gcp',     
    'warehouse': 'COMPUTE_WH',
    'database': 'demo',
    'schema': 'PUBLIC'
}

class Student(BaseModel):
    id: int
    name: str
    department: str


def get_connection():
    return snowflake.connector.connect(**conn_params) # snowflake connection

@app.get("/students") # get all students
def get_students():
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, department FROM student")
        rows = cur.fetchall()
        students = [{"id": r[0], "name": r[1], "department": r[2]} for r in rows]
        return {"students": students}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()