from fastapi import FastAPI
from sqlalchemy import create_engine

app = FastAPI()

DATABASE_URL = "mysql+pymysql://root:root@grading_db:3306/grading_db"
engine = create_engine(DATABASE_URL)

@app.get("/")
def home():
    return {"message": "Grading Service Running"}

@app.get("/health")
def health_check():
    try:
        with engine.connect() as conn:
            return {"status": "ok", "db": "connected"}
    except Exception as e:
        return {"status": "error", "details": str(e)}
