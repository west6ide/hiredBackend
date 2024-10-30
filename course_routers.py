from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import CourseCreate, CourseUpdate, CourseRead, LessonCreate, LessonUpdate, LessonRead
from models import Course, Lesson
from settings import get_db

course_router = APIRouter(prefix="/courses", tags=["Courses"])
lesson_router = APIRouter(prefix="/courses/{course_id}/lessons", tags=["Lessons"])

# Course Endpoints
@course_router.post("/create", response_model=CourseRead)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    new_course = Course(**course.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@course_router.get("/{course_id}", response_model=CourseRead)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@course_router.put("/update/{course_id}", response_model=CourseRead)
def update_course(course_id: int, course: CourseUpdate, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    for key, value in course.dict(exclude_unset=True).items():
        setattr(db_course, key, value)
    db.commit()
    db.refresh(db_course)
    return db_course

@course_router.delete("/delete/{course_id}", response_model=CourseRead)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(db_course)
    db.commit()
    return db_course

# Lesson Endpoints
@lesson_router.post("/", response_model=LessonRead)
def create_lesson(course_id: int, lesson: LessonCreate, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    new_lesson = Lesson(**lesson.dict(), course_id=course_id)
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    return new_lesson

@lesson_router.get("/{lesson_id}", response_model=LessonRead)
def get_lesson(course_id: int, lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id, Lesson.course_id == course_id).first()
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson

@lesson_router.put("/update/{lesson_id}", response_model=LessonRead)
def update_lesson(course_id: int, lesson_id: int, lesson: LessonUpdate, db: Session = Depends(get_db)):
    db_lesson = db.query(Lesson).filter(Lesson.id == lesson_id, Lesson.course_id == course_id).first()
    if db_lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    for key, value in lesson.dict(exclude_unset=True).items():
        setattr(db_lesson, key, value)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

@lesson_router.delete("/delete/{lesson_id}", response_model=LessonRead)
def delete_lesson(course_id: int, lesson_id: int, db: Session = Depends(get_db)):
    db_lesson = db.query(Lesson).filter(Lesson.id == lesson_id, Lesson.course_id == course_id).first()
    if db_lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    db.delete(db_lesson)
    db.commit()
    return db_lesson
