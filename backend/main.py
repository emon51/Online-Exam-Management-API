from fastapi import FastAPI, Depends, HTTPException, Request, UploadFile
import schemas 
from database import SessionLocal, Base, engine
from sqlalchemy.orm import Session
import models
import openpyxl
import json
from io import BytesIO
from typing import List, Optional

app = FastAPI(title="Online Exam Management API.")

Base.metadata.create_all(bind=engine)

# To get DB session.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#========================================================================================
# Helper functions.

def parse_excel(file_obj):
    wb = openpyxl.load_workbook(file_obj)
    sheet = wb.active

    rows = []

    for row in sheet.iter_rows(min_row=2, values_only=True):
        rows.append({
            "title": row[0],
            "type": row[1],
            "complexity": row[2],
            "options": row[3],
            "correct_answers": row[4],
            "max_score": row[5]
        })

    return rows
#==================================================================
@app.get('/')
async def index():
    return {"message": "Welcome."}

@app.post('/signup')
async def signup(user: schemas.UserModel, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=403, detail="Already registered.")
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    return db_user 

@app.get('/users')
async def users(db: Session=Depends(get_db)):
    all_users = db.query(models.User).all()
    if all_users:
        return all_users 
    else:
        raise HTTPException(status_code=404, detail="No users found.")
    

@app.post("/login")
async def user_login(user: schemas.LoginModel, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")
    if user.password != db_user.password:
        raise HTTPException(status_code=400, detail="Invalid password.")
        
    return {"message": f"Welcome {db_user.username}", "user_id": db_user.id, "role": db_user.role}

    

@app.get("/questions/list")
async def questions(db: Session = Depends(get_db)):
    all_questions = db.query(models.Question).all()
    if all_questions:
        return all_questions
    else:
        raise HTTPException(status_code=404, detail="No questions found.")
    


@app.post("/questions/upload-xlsx")
async def upload_questions(file: UploadFile, db: Session = Depends(get_db)):
    content = await file.read()
    data = parse_excel(BytesIO(content))
    for q in data:
        db_question = models.Question(
            title=q["title"],
            type=q["type"],
            complexity=q["complexity"],
            options=json.loads(q["options"]) if q["options"] else None,
            correct_answers=json.loads(q["correct_answers"]) if q["correct_answers"] else None,
            max_score=q["max_score"]
        )
        db.add(db_question)

    db.commit()

    return {"message": "Questions uploaded successfully."}



@app.post("/exams/create")
async def create_exam(exm: schemas.ExamCreate, db: Session = Depends(get_db)):
    exam = models.Exam(**exm.dict())
    db.add(exam)
    db.commit()
    return {"message": "Exam created successfully."}



@app.get("/exams/list")
async def questions(db: Session = Depends(get_db)):
    all_exams = db.query(models.Exam).all()
    if all_exams:
        return all_exams
    else:
        raise HTTPException(status_code=404, detail="No exams found.")


# add questions to exam.
@app.post("/exams/{exam_id}/add-questions")
def add_questions_to_exam(exam_id: str, question_ids: List[str], db: Session = Depends(get_db)):
    exam = db.query(models.Exam).filter(models.Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    for qid in question_ids:
        link = models.ExamQuestion(exam_id=exam_id, question_id=qid)
        db.add(link)
    db.commit()
    return {"message": "Questions added to the exam."}


@app.get("/exams/exam-question-list")
async def questions(db: Session = Depends(get_db)):
    all_records = db.query(models.ExamQuestion).all()
    if all_records:
        return all_records
    else:
        raise HTTPException(status_code=404, detail="Not found.")



