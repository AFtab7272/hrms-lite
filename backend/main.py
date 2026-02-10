from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, SessionLocal

# ---------------- APP INIT ----------------
app = FastAPI(
    title="HRMS Lite API",
    docs_url="/docs",        # 🔥 force swagger
    redoc_url="/redoc"
)

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://relaxed-empanada-270748.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- DB INIT ----------------
models.Base.metadata.create_all(bind=engine)

# ---------------- DB DEP ----------------
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

# ---------------- SEED (🔥 IMPORTANT) ----------------
@app.post("/seed")
def seed_data(db: Session = Depends(get_db)):
    if db.query(models.Employee).count() > 0:
        return {"message": "Employees already exist"}

    emp = models.Employee(
        employee_id="EMP001",
        full_name="Aftab Ansari",
        email="aftab@example.com",
        department="Engineering"
    )

    db.add(emp)
    db.commit()
    return {"message": "Seed data added"}

# ---------------- EMPLOYEES ----------------
@app.post("/employees", response_model=schemas.EmployeeResponse)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    if db.query(models.Employee).filter(
        models.Employee.employee_id == employee.employee_id
    ).first():
        raise HTTPException(status_code=400, detail="Employee already exists")

    emp = models.Employee(**employee.dict())
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp


@app.get("/employees", response_model=list[schemas.EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    return db.query(models.Employee).all()

# ---------------- ATTENDANCE ----------------
@app.post("/attendance", response_model=schemas.AttendanceResponse)
def mark_attendance(att: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    emp = db.query(models.Employee).filter(models.Employee.id == att.employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    record = models.Attendance(**att.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@app.get("/attendance/{employee_id}", response_model=list[schemas.AttendanceResponse])
def get_attendance(employee_id: int, db: Session = Depends(get_db)):
    return db.query(models.Attendance).filter(
        models.Attendance.employee_id == employee_id
    ).all()
