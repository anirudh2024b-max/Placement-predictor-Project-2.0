from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import create_table, get_connection
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_table()
class Application(BaseModel):
    name: str
    role: str
    date_applied: str
    company: str
    cgpa: float

applications = [
    {
        "name": "Ramesh",
        "role": "Web-Dev",
        "date_applied": "29-06-2026",
        "company": "TCS",
        "cgpa": 7.2
    },
    {
        "name": "Ganesh",
        "role": "Full-Stack",
        "date_applied": "12-04-2026",
        "company": "Fargo",
        "cgpa": 6.0
    }
]

@app.get("/")
def home():
     return FileResponse("static/PlacementTracker.html")

@app.get("/applications")
def get_applications():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM applications")

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]

@app.get("/eligibility/{cgpa}")
def check_eligibility(cgpa: float):
    if cgpa >= 6.5:
        return {"status": "Eligible"}
    else:
        return {"status": "Not Eligible"}

@app.post("/applications")
def add_application(application: Application):

    # Automatically decide the status
    if application.cgpa >= 6.5:
        status = "Selected"
    else:
        status = "Rejected"

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO applications(name, role, date_applied, company, cgpa, status)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (
        application.name,
        application.role,
        application.date_applied,
        application.company,
        application.cgpa,
        status
    ))

    conn.commit()
    conn.close()

    return {
        "message": "Application Added Successfully",
        "status": status
    }