from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI()

# Database URL (use docker-compose service name "course_db")
DATABASE_URL = "mysql+pymysql://root:root@course_db:3306/course_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Example model
class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.get("/courses")
def list_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

@app.post("/courses")
def add_course(title: str, description: str = None, db: Session = Depends(get_db)):
    course = Course(title=title, description=description)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course
