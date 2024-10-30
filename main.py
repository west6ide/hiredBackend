from fastapi import HTTPException, Request
from starlette.responses import JSONResponse

from settings import Base, engine
from fastapi import FastAPI
from course_routers import course_router, lesson_router

app = FastAPI(title="Course API", description="API для управления курсами и уроками")

app.include_router(course_router)
app.include_router(lesson_router)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Welcome to the Course API!"}


@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "An unexpected error occurred"})
