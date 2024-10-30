from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from settings import Base

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    lessons = relationship("Lesson", back_populates="course")

class Lesson(Base):
    __tablename__ = 'lessons'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    course_id = Column(Integer, ForeignKey('courses.id'))
    course = relationship("Course", back_populates="lessons")
