from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, SessionLocal

# ---------------- APP INIT ----------------
app = FastAPI(
    title="HRMS Lite API",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# ---------------- CORS CONFIG ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://relaxed-empanada-270748.netlify.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- DB INIT ----------------
models.Base.metadata.create_all(bind=engine)

# ---------------- DB DEPENDENCY ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {"message": "HRMS Lite Backend Running"}

# ---------------- EMPLOYEE APIs ----------------

@app.post("/employees", response_model=schemas.EmployeeResponse)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Employee).filter(
        models.Employee.employee_id == employee.employee_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Employee ID already exists")

    emp = models.Employee(**employee.dict())
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp


@app.get("/employees", response_model=list[schemas.EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    return db.query(models.Employee).all()


# ---------------- ATTENDANCE APIs ----------------

@app.post("/attendance", response_model=schemas.AttendanceResponse)
def mark_attendance(attendance: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    emp = db.query(models.Employee).filter(
        models.Employee.id == attendance.employee_id
    ).first()

    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    att = models.Attendance(**attendance.dict())
    db.add(att)
    db.commit()
    db.refresh(att)
    return att


@app.get("/attendance/{employee_id}", response_model=list[schemas.AttendanceResponse])
def get_attendance(employee_id: int, db: Session = Depends(get_db)):
    return db.query(models.Attendance).filter(
        models.Attendance.employee_id == employee_id
    ).all()
