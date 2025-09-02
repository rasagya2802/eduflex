from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
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

from fastapi.middleware.cors import CORSMiddleware
import logging

# Allow frontend React app to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change later to ["http://localhost:3000"] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple logging middleware
@app.middleware("http")
async def log_requests(request, call_next):
    logging.info(f"➡️ Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logging.info(f"⬅️ Response status: {response.status_code}")
    return response


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ====================
# Database Model
# ====================
class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)

Base.metadata.create_all(bind=engine)

# ====================
# Schemas
# ====================
class CourseCreate(BaseModel):
    title: str
    description: str | None = None

class CourseOut(BaseModel):
    id: int
    title: str
    description: str | None = None

    class Config:
        orm_mode = True

# ====================
# Dependency
# ====================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ====================
# CRUD Endpoints
# ====================

@app.get("/courses", response_model=list[CourseOut])
def list_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

@app.get("/courses/{course_id}", response_model=CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.post("/courses", response_model=CourseOut, status_code=201)
def add_course(course: CourseCreate, db: Session = Depends(get_db)):
    new_course = Course(title=course.title, description=course.description)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@app.put("/courses/{course_id}", response_model=CourseOut)
def update_course(course_id: int, course_data: CourseCreate, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    course.title = course_data.title
    course.description = course_data.description
    db.commit()
    db.refresh(course)
    return course

@app.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    return {"message": "Course deleted"}
