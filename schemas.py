from pydantic import BaseModel
from typing import List, Optional

# Course Schemas

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class CourseRead(CourseBase):
    id: int
    lessons: List['LessonRead'] = []


    class Config:
        from_attributes = True


# Lesson Schemas

class LessonBase(BaseModel):
    title: str
    content: Optional[str] = None

class LessonCreate(LessonBase):
    pass

class LessonUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class LessonRead(LessonBase):
    id: int
    course_id: int

    class Config:
        orm_mode = True
