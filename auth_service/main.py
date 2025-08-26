from fastapi import FastAPI
from sqlalchemy import create_engine

app = FastAPI()

# MySQL DB connection (auth_db from docker-compose)
DATABASE_URL = "mysql+pymysql://root:root@auth_db:3306/auth_db"
engine = create_engine(DATABASE_URL)

@app.get("/")
def home():
    return {"message": "Auth Service Running"}

@app.get("/health")
def health_check():
    try:
        with engine.connect() as conn:
            return {"status": "ok", "db": "connected"}
    except Exception as e:
        return {"status": "error", "details": str(e)}
