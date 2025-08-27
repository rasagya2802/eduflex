from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import time

DATABASE_URL = "mysql+pymysql://root:root@course_db:3306/course_db"

# Retry DB connection
for i in range(10):
    try:
        engine = create_engine(DATABASE_URL, echo=True, future=True)
        connection = engine.connect()
        connection.close()
        break
    except Exception as e:
        print("DB not ready, retrying...", e)
        time.sleep(3)
else:
    raise Exception("Database not available after 10 retries")

app = FastAPI()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ✅ Example model
class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)

# ✅ Create tables after defining models
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Routes
@app.get("/courses")
def list_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return [{"id": c.id, "title": c.title, "description": c.description} for c in courses]

@app.post("/courses")
def add_course(title: str, description: str = None, db: Session = Depends(get_db)):
    course = Course(title=title, description=description)
    db.add(course)
    db.commit()
    db.refresh(course)
    return {"id": course.id, "title": course.title, "description": course.description}
